from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.utils.afisha import get_all_events
from bot.utils.chats import chat

router = Router()


@router.message(Command(commands=["events"]))
async def start_chat(message: Message, state: FSMContext):
    """
    Обработчик команды /events. Загружает мероприятия с сайта и выводит их.
    """
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    events_text = get_all_events()

    events_text += "ты отправила мне список, значит напиши про грядущие несколько событий которые будут проходить скоро."
    user_name = message.from_user.first_name
    bot_response = await chat(user_name=user_name, user_input=events_text, clear=True)
    await message.answer(bot_response)
