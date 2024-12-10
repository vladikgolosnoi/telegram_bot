from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.types import Message

from bot.States.chat import ChatStates
from bot.handlers.chat.utils.escape import escape_markdown
from bot.utils.chats import chat
from bot.handlers.chat.utils.extract_user import extract_user_input
from bot.handlers.chat.utils.send_response import send_default_response

router = Router()


@router.message(ChatStates.waiting_for_user_message)
async def handle_chat(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    user_id = str(message.from_user.id)

    # Проверка входного сообщения
    user_input = extract_user_input(message)
    if not user_input:
        return await send_default_response(message, user_id)

    # Обработка обычного чата
    bot_response = await chat(user_name=user_id, user_input=user_input)
    escaped_text = escape_markdown(bot_response)
    await message.answer(escaped_text, parse_mode="Markdown")
