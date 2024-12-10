from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.map import get_map_keyboard
from bot.utils.chats import chat

router = Router()


@router.message(Command(commands=["map"]))
async def start_map(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Ответное сообщение
    user_id = str(message.from_user.id)
    text = "Напиши текст о том что нажмите на карту ростова внизу, чтобы выбрать заведение:"
    bot_response = await chat(user_name=user_id, user_input=text, clear=True)
    await message.answer(bot_response, reply_markup=get_map_keyboard())
