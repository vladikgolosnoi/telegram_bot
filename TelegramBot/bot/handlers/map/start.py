from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.map import get_map_keyboard
from bot.utils.chats import chat

router = Router()


@router.message(Command(commands=["map"]))
async def start_map(message: Message):
    # Показываем индикатор "набор текста"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Ответное сообщение
    user_id = str(message.from_user.id)
    text = (
        "Нажмите на кнопку \"Открыть карту 🌍\" ниже, чтобы выбрать заведение на карте Ростова. "
    )
    # Отправляем сообщение с клавиатурой
    await message.answer(text, reply_markup=get_map_keyboard())
