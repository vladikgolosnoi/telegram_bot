import requests
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.chats import chat

router = Router()


# Функция для получения прогноза погоды с использованием бесплатного сервиса wttr.in
def get_weather(city: str = "Rostov-on-Don") -> str:
    """Получаем погоду из wttr.in (бесплатный сервис без API ключа)."""
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Извлекаем нужные данные о погоде
        current_weather = data['current_condition'][0]
        temperature = current_weather['temp_C']
        feels_like = current_weather['FeelsLikeC']
        humidity = current_weather['humidity']
        wind_speed = current_weather['windspeedKmph']

        weather_text = (
            f"🌤️ Погода в {city}:\n"
            f"🌡️ Температура: {temperature}°C (ощущается как {feels_like}°C)\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬️ Ветер: {wind_speed} км/ч"
        )
        return weather_text + "информацию о погоде выводи со смайликами через отступы"
    except Exception as e:
        print(e)
        return f"❌ Ошибка при получении прогноза погоды: {e}"


@router.message(Command(commands="weather"))
async def cmd_weather(message: Message):
    """
    Команда /weather.
    1. Отправляем "печатает...".
    2. Получаем погоду.
    3. Бот сам пишет погоду.
    """
    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Получаем текст прогноза погоды
    weather_text = get_weather()

    # Эмуляция ответа бота, как будто GPT отправляет текст
    user_name = message.from_user.first_name
    bot_response = await chat(user_name=user_name, user_input=weather_text, clear=True)

    # Отправляем сообщение с погодой
    await message.answer(text=bot_response)

