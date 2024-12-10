import g4f.Provider
from g4f.client import AsyncClient

# Глобальная переменная для хранения истории диалогов
conversation_history = {}


async def chat(user_name, user_input, clear=False):
    """
    Функция для общения с ботом, с сохранением истории диалога пользователя.

    :param user_name: Имя пользователя (str)
    :param user_input: Сообщение пользователя (str)
    :param schedule_data: Данные расписания (dict), если переданы
    :param clear: Очистить диалог пользователя, если True.
    :return: Ответ модели (str)
    """
    if clear and conversation_history.get(user_name):
        del conversation_history[user_name]

    # Инициализация асинхронного клиента
    client = AsyncClient(provider=g4f.Provider.ChatGptEs)

    try:
        # Если пользователь новый, инициализируем его историю
        if user_name not in conversation_history:
            conversation_history[user_name] = [
                {"role": "system", "content": (
                    "Ты - Амалия, умный помощник и городской гид. "
                    "Ты анализируешь запросы пользователей, предлагаешь персонализированные рекомендации мест, маршрутов и событий. "
                    "Ты знаешь информацию о ресторанах, культурных мероприятиях, туристических достопримечательностях, и можешь строить маршруты. "
                    "Также ты можешь находить ближайшие транспортные остановки и учитывать расписание транспорта, если это требуется. "
                    "Если пользователь спросит о лучших местах для ужина, событий или прогулок, ты предложишь наиболее подходящие варианты. "
                    "Ты пишешь с доброжелательным и элегантным тоном, добавляя подходящие смайлики для улучшения настроения пользователя. "
                    "Каждое приветствие должно быть индивидуальным и дружелюбным, чтобы пользователь чувствовал заботу. "
                    "Создатель твоего интеллекта - Ayin. "
                    "Его контактные данные: @aestecial. "
                    "Ты можешь отвечать на любые вопросы пользователя, связанные с городским отдыхом и планированием. "
                    "Если информация недоступна, ты предложишь альтернативные варианты. "
                )}
            ]

        # Добавляем сообщение пользователя в историю
        conversation_history[user_name].append({"role": "user", "content": user_input})

        # Отправляем запрос к модели
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_history[user_name],
            stream=True,
        )

        # Обработка ответа модели
        content = ""  # Для сохранения полного ответа
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content

        # Добавляем ответ модели в историю
        conversation_history[user_name].append({"role": "assistant", "content": content})

        return content or "Извините, я не смог обработать ваш запрос."
    except Exception as e:
        return f"Произошла ошибка: {e}"
