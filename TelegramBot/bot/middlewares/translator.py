import os
import json
from aiogram import BaseMiddleware
from aiogram.types import Message

class Translator:
    def __init__(self, translations: dict, default_locale: str = "en"):
        self.translations = translations
        self.default_locale = default_locale

    def translate(self, language: str, key: str, **kwargs) -> str:
        if language not in self.translations:
            language = self.default_locale

        message = self.translations[language].get(key, key)
        return message.format(**kwargs)


class TranslationMiddleware(BaseMiddleware):
    def __init__(self, locales_dir: str, default_locale: str = "en"):
        self.locales_dir = locales_dir
        self.default_locale = default_locale
        self.translations = self.load_translations()
        self.translator = Translator(self.translations, default_locale)
        super().__init__()

    def load_translations(self) -> dict:
        translations = {}
        for file_name in os.listdir(self.locales_dir):
            if file_name.endswith(".json"):
                locale = file_name.split(".")[0]  # Имя файла без расширения (например, en, ru)
                file_path = os.path.join(self.locales_dir, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    translations[locale] = json.load(f)  # Загружаем JSON
        return translations

    async def __call__(self, handler, event: Message, data: dict):
        user_language = event.from_user.language_code or self.default_locale

        data["translator"] = self.translator
        data["locale"] = user_language

        return await handler(event, data)
