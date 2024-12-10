from aiogram.types import Message

from bot.utils.chats import chat


async def send_default_response(message: Message, user_id: str):
    response = "Не могу обработать этот запрос. Отправьте текстовое сообщение."
    bot_response = await chat(user_name=user_id, user_input=response)
    await message.answer(bot_response, parse_mode="Markdown")
