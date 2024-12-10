from aiogram.types import Message


def extract_user_input(message: Message):
    if message.text:
        return message.text.strip()
    return None
