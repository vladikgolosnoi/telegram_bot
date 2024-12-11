from aiogram import Dispatcher
from bot.handlers.start.start import router as start_router
from bot.handlers.help.help import router as help_router
from bot.handlers.chat.start import router as start_chat_router
from bot.handlers.chat.chat import router as chat_router
from bot.handlers.weather.start import router as weather_router
from bot.handlers.map.start import router as map_router


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(map_router)
    dp.include_router(weather_router)
    dp.include_router(start_chat_router)
    dp.include_router(chat_router)
