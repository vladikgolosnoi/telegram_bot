import random
import json
import pandas as pd
from fuzzywuzzy import fuzz  # Импорт функции для сравнения строк

# Чтение всех вкладок из Excel-файла
file_path = 'data/places.xlsx'
sheets = pd.read_excel(file_path, sheet_name=None)

# Парсинг данных из каждой вкладок Excel и преобразование в общий словарь
places_data = {}
for sheet_name, df in sheets.items():
    if not df.empty:
        df = df.rename(columns={
            "Название": "название",
            "Описание": "описание",
            "Местоположение": "адрес",
            "Карта": "карта"
        })
        places_data[sheet_name.lower()] = df.to_dict(orient="records")


# Функция для получения данных о конкретной достопримечательности
def get_place_details(query=None):
    """
    Функция для поиска данных о достопримечательности по запросу.
    Ищет совпадение по частям (словам) из запроса и останавливается, как только находит одно точное совпадение.
    """
    if query:  # Проверяем, есть ли запрос
        # Приведение запроса к нижнему регистру и разбивка на слова
        query_words = query.lower().split()

        best_match = None
        best_score = 0

        # Поиск совпадений по каждому слову во всех категориях
        for word in query_words:  # Перебираем каждое слово из запроса
            for category, places in places_data.items():
                for place in places:
                    place_name = place['название'].lower()
                    # Сравниваем схожесть слова из запроса и названия места
                    similarity_score = fuzz.partial_ratio(word, place_name)
                    if similarity_score > best_score:
                        best_score = similarity_score
                        best_match = place

                    # Если совпадение высокое, сразу возвращаем место
                    if similarity_score > 80:  # Порог для быстрого выхода
                        return (
                            f"Вот информация о месте '{place['название']}':\n"
                            f"Описание: {place['описание']}\n"
                            f"Адрес: {place['адрес']}\n"
                            f"Карта: {place['карта']}"
                        )

        # Если найдено хорошее совпадение, возвращаем его
        if best_match and best_score > 60:  # Порог схожести для совпадения (можно менять)
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
        f"Вот случайная достопримечательность:\n"
        f"Название: {random_place['название']}\n"
        f"Описание: {random_place['описание']}\n"
        f"Адрес: {random_place['адрес']}\n"
        f"Карта: {random_place['карта']}"
    )

# Пример использования
query = "хочу глянуть склады какие то"  # Пример запроса
response = get_place_details(query)
print(response)
