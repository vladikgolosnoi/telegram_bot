import os
import json


class Translator:
    def __init__(self, translations: dict, default_locale: str = "en"):
        self.translations = translations
        self.default_locale = default_locale

    def translate(self, language: str, key: str, **kwargs) -> str:
        if language not in self.translations:
            language = self.default_locale

        message = self.translations[language].get(key, key)
        return message.format(**kwargs)


def load_translations(locales_dir: str) -> dict:
    translations = {}
    for file_name in os.listdir(locales_dir):
        if file_name.endswith(".json"):
            locale = file_name.split(".")[0]
            file_path = os.path.join(locales_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                translations[locale] = json.load(f)
    return translations
