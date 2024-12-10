from aiogram.fsm.state import StatesGroup, State


class ChatStates(StatesGroup):
    waiting_for_user_message = State()  # Ожидаем сообщение пользователя
