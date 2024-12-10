# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app/tg_bot

# Копируем файлы в контейнер
COPY . /app/tg_bot

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файл .env
COPY .env /app/tg_bot/.env

# Делаем скрипт запуска исполняемым
RUN chmod +x run.sh

# Устанавливаем команду запуска
CMD ["./run.sh"]
