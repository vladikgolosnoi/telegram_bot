from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.States.chat import ChatStates
from bot.utils.chats import chat

router = Router()


@router.message(Command(commands=["chat"]))
async def start_chat(message: Message, state: FSMContext):
    """
    Обработчик команды /chat. Начинает диалог и переводит пользователя в состояние ожидания сообщения.
    """
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    user_id = str(message.from_user.id)
    text = "Привет! Как тебя зовут? И что ты умеешь?"
    bot_response = await chat(user_name=user_id, user_input=text, clear=True)
    await message.answer(bot_response)
    await state.set_state(ChatStates.waiting_for_user_message)
