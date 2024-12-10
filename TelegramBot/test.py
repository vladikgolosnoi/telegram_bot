import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Ваш API-ключ Яндекс.Карт
YANDEX_API_KEY = 'e2361bc5-4b9a-4489-a803-5594fe96b3e8'

# Токен вашего Telegram-бота
TELEGRAM_BOT_TOKEN = '7345214682:AAGYBO_tkNnxKbyvw2qW5_nBQ834TQJmOh4'


async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(handle_message)
    await dp.start_polling(bot)


def search_places(query):
    url = f"https://search-maps.yandex.ru/v1/?text={query}&lang=ru_RU&apikey={YANDEX_API_KEY}"
    response = requests.get(url)
    data = response.json()

    places = []
    for place in data.get('features', [])[:3]:
        name = place['properties']['name']
        rating = place['properties'].get('CompanyMetaData', {}).get('rating', 'Нет рейтинга')
        description = place['properties'].get('description', 'Нет описания')
        places.append({'name': name, 'rating': rating, 'description': description})

    return places


async def send_welcome(message: Message):
    await message.reply(
        "Привет! Я бот, который поможет тебе найти места. Просто напиши, что ты ищешь, например, 'грузинское кафе'.")


async def handle_message(message: Message):
    query = message.text
    places = search_places(query)

    if places:
        response = ""
        for i, place in enumerate(places, 1):
            response += f"{i}. {place['name']}\nРейтинг: {place['rating']}\nОписание: {place['description']}\n\n"
        await message.reply(response)
    else:
        await message.reply("К сожалению, по вашему запросу ничего не найдено. Попробуйте уточнить запрос.")



if __name__ == '__main__':
    asyncio.run(main())