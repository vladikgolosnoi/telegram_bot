from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, translator, locale):
    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Генерируем текст ответа
    text = translator.translate(locale, "start_message", name=message.from_user.first_name)

    # Отправляем сообщение
    await message.answer(text=text)
