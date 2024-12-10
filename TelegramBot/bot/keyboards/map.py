from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# URL карты
MAP_URL = "https://devayin.ru/"

def get_map_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопкой для открытия карты.
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Открыть карту 🌍", web_app=WebAppInfo(url=MAP_URL))
            ]
        ]
    )
    return keyboard
