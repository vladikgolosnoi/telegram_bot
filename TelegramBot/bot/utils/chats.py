import random
import json
import pandas as pd
from fuzzywuzzy import fuzz  # Импорт функции для сравнения строк
import g4f.Provider
from g4f.client import AsyncClient

# Глобальная переменная для хранения истории диалогов
conversation_history = {}

# Загрузка базы данных из Excel
places_data = {}

# Чтение всех вкладок из Excel-файла
try:
    sheets = pd.read_excel('data/places.xlsx', sheet_name=None)  # Укажите путь к вашему Excel-файлу
    for sheet_name, df in sheets.items():
        if not df.empty:
            df = df.rename(columns={
                "Название": "название",
                "Описание": "описание",
                "Местоположение": "адрес",
                "Карта": "карта",
                "Теги": "теги"
            }).fillna("")
            if "теги" in df.columns:
                df["теги"] = df["теги"].apply(lambda x: x.split(",") if x else [])
            places_data[sheet_name.lower()] = df.to_dict(orient="records")
except FileNotFoundError:
    print("Файл data/places.xlsx не найден")


def get_all_categories_and_places():
    """
    Функция для вывода всех категорий и их данных.
    """
    if not places_data:
        return "Данные о местах не загружены."

    response = "Вот все доступные категории и их данные:\n"
    for category, places in places_data.items():
        response += f"\nКатегория: {category.capitalize()}\n"
        response += "-" * 30 + "\n"
        for i, place in enumerate(places, start=1):
            response += (
                f"{i}. {place.get('название', 'Без названия')}\n"
                f"Описание: {place.get('описание', 'Описание отсутствует')}\n"
                f"Адрес: {place.get('адрес', 'Адрес отсутствует')}\n"
                f"Карта: {place.get('карта', 'Ссылка на карту отсутствует')}\n"
            )
            # Добавляем теги, если они есть
            if "теги" in place and place['теги']:
                response += f"Теги: {', '.join(place['теги'])}\n"
            else:
                response += "Теги: Нет тегов\n"
            response += "\n"  # Разделитель между местами
    return response.strip()



def get_restaurants_by_tags(query_tags):
    """
    Функция для поиска ресторанов по тегам, включая похожие теги.
    """
    results = []
    for place in places_data.get("рестораны", []):  # Обрабатываем только категорию "рестораны"
        for tag in query_tags:
            for place_tag in place['теги']:
                similarity_score = fuzz.partial_ratio(tag.lower(), place_tag.lower())
                if similarity_score > 70:  # Условие совпадения по тегу
                    results.append(place)
                    break
    return results[:5]  # Лимитируем количество результатов


def get_random_places_from_category(category, count=3):
    """
    Возвращает случайные места из указанной категории.
    """
    category = category.lower()
    if category in places_data and len(places_data[category]) > 0:
        chosen = random.sample(places_data[category], min(count, len(places_data[category])))
        response = f"Вот несколько мест из категории '{category}':\n"
        for i, place in enumerate(chosen, start=1):
            response += (
                f"{i}. {place['название']} - {place['адрес']}\n"
                f"Описание: {place['описание']}\n\n"
            )
        return response.strip()
    return f"К сожалению, не удалось найти места в категории '{category}'."


def get_place_details(query=None):
    """
    Функция для поиска данных о достопримечательности по запросу.
    Ищет совпадение по названию места.
    """
    if query:
        query_lower = query.lower()

        # Прямой поиск по названию
        best_match = None
        best_score = 0

        for category, places in places_data.items():
            for place in places:
                place_name = place['название'].lower()
                similarity_score = fuzz.partial_ratio(query_lower, place_name)
                if similarity_score > best_score:
                    best_score = similarity_score
                    best_match = place

                # Если совпадение высокое, сразу возвращаем место
                if similarity_score > 80:
                    return (
                        f"Вот информация о месте '{place['название']}':\n"
                        f"Описание: {place['описание']}\n"
                        f"Адрес: {place['адрес']}\n"
                        f"Карта: {place['карта']}"
                    )

        # Если найдено хорошее совпадение, возвращаем его
        if best_match and best_score > 60:
            return (
                f"Вот информация о месте '{best_match['название']}':\n"
                f"Описание: {best_match['описание']}\n"
                f"Адрес: {best_match['адрес']}\n"
                f"Карта: {best_match['карта']}"
            )

    # Если запрос пустой или ничего не найдено, возвращаем случайную достопримечательность
    random_category = random.choice(list(places_data.keys()))
    random_place = random.choice(places_data[random_category])
    return (
        f"Название: {random_place['название']}\n"
        f"Описание: {random_place['описание']}\n"
        f"Адрес: {random_place['адрес']}\n"
        f"Карта: {random_place['карта']}"
    )


def find_best_category(query):
    """Находит наиболее подходящую категорию по запросу с использованием fuzzywuzzy."""
    query_lower = query.lower()
    best_match = None
    best_score = 0
    for cat in places_data.keys():
        similarity_score = fuzz.partial_ratio(query_lower, cat)
        if similarity_score > best_score:
            best_score = similarity_score
            best_match = cat
    if best_score > 70:  # Порог совпадения
        return best_match
    return None


async def chat(user_name, user_input, clear=False):
    if clear and conversation_history.get(user_name):
        del conversation_history[user_name]

    client = AsyncClient(provider=g4f.Provider.ChatGptEs)

    try:
        if user_name not in conversation_history:
            conversation_history[user_name] = [
                {"role": "system", "content": (
                    "Ты - Амалия, умный помощник и городской гид. "
                    "Ты анализируешь запросы пользователей, предлагаешь персонализированные рекомендации мест, маршрутов и событий в Ростове-на-Дону."
                    f"Тебе известны данные {get_all_categories_and_places()}. Рекомендуй по ним и показывай адрес где находится и ссылку(полную ссылку, не меняй ее и бери из этих данных)."
                    "Ограничься 2 местами и пиши красиво, дополняй."
                    "Пиши элегантно и с эмодзи."
                )}
            ]

        # Определяем категорию на основе пользовательского ввода
        found_category = find_best_category(user_input)

        # Логика для поиска по категории
        trigger_words2 = ["расскажи", "найди", "покажи"]

        if any(word in user_input.lower() for word in trigger_words2):
            # Если категория не найдена, пытаемся найти конкретное место по названию
            user_input = get_place_details(user_input) + \
                         "\n эти все данные отправила ты - просто напиши о них в красивом виде через отступы. Напиши описание и добавь что-то свое туда. Не забудь оставить ссылки на карту яндекса."
        elif found_category:
            # Если найдена категория, показываем случайное место из категории
            user_input = get_random_places_from_category(found_category, count=1) + \
                         "\n эти все данные отправила ты - просто напиши о них в красивом виде через отступы. Напиши описание и добавь что-то свое туда. Не забудь оставить ссылки на карту яндекса."

        # Сохраняем пользовательский запрос
        conversation_history[user_name].append({"role": "user", "content": user_input})

        # Обработка с помощью g4f
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_history[user_name],
            stream=True,
        )

        content = ""  # Для сохранения полного ответа
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content

        # Сохраняем ответ ассистента
        conversation_history[user_name].append({"role": "assistant", "content": content})
        return content or "Извините, я не смог обработать ваш запрос."
    except Exception as e:
        return f"Произошла ошибка: {e}"
