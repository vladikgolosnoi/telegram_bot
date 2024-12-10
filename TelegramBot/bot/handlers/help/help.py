from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.types import Message
from aiogram.filters import Command

from bot.middlewares.translator import Translator

router = Router()


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, translator: Translator, locale):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    text = translator.translate(locale, "help_message")
    await message.answer(text=text)

