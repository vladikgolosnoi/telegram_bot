import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.config import load_config, Config
from bot.handlers import register_handlers

from bot.middlewares.translator import TranslationMiddleware

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Функция для установки команд в меню
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать общение с ботом"),
        BotCommand(command="events", description="Узнать грядущие события"),
        BotCommand(command="map", description="Открыть карту"),
        BotCommand(command="weather", description="Погода в Ростове"),
    ]
    await bot.set_my_commands(commands)


# Основная функция
async def main():
    config: Config = load_config()  # Загрузка конфига

    # Создаем бота и диспетчера
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(
            parse_mode="markdown",
            link_preview_is_disabled=True,
        )
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Загружаем локализацию
    dp.message.middleware(TranslationMiddleware(locales_dir=config.locales))

    # Регистрируем обработчики
    register_handlers(dp)

    # Устанавливаем команды в меню
    await set_bot_commands(bot)

    # Запуск бота
    try:
        await dp.start_polling(bot)
    except Exception as err:
        logger.error(f"Не удалось запустить бота - {err}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
