from dataclasses import dataclass

from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()

# Настройка локализации
LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")

@dataclass
class Config:
    bot_token: str
    locales: str



def load_config() -> Config:
    return Config(
        bot_token=os.getenv("BOT_TOKEN"),
        locales=LOCALES_DIR,
    )
