# Telegram Bot

Этот репозиторий содержит Telegram-бота, созданного с использованием библиотеки [aiogram](https://docs.aiogram.dev/). Вы можете запустить бота локально или внутри Docker-контейнера.

## Важно!

После клонирования репозитория переименуйте файл `.envexample` в `.env` и добавьте токен, полученный от [BotFather](https://t.me/BotFather). 

Пример содержимого файла `.env`:
```env
BOT_TOKEN=ваш-токен-бота
```

## Содержание

- [Запуск бота локально](#запуск-бота-локально)
- [Запуск бота через Docker](#запуск-бота-через-docker)
- [Гайд для пользователей Windows/MacOS](#гайд-для-пользователей-windowsmacos)

## Запуск бота локально

### Предварительные требования

Убедитесь, что у вас установлены следующие инструменты:

- Python 3.10 или выше
- pip (менеджер пакетов Python)
- Git (необязательно, для клонирования репозитория)

### Шаги установки для пользователей Linux

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/telegram-bot.git
   cd telegram-bot/TelegramBot
   ```

2. Создайте виртуальное окружение (рекомендуется):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env`:
   Скопируйте пример файла окружения и добавьте токен вашего бота.
   ```bash
   cp .envexample .env
   ```

   **Пример файла `.env`:**
   ```env
   BOT_TOKEN=ваш-токен-бота
   ```

### Запуск бота

1. Активируйте виртуальное окружение (если оно не было активировано):
   ```bash
   source venv/bin/activate
   ```

2. Запустите бота:
   ```bash
   python main.py
   ```

3. Откройте Telegram и начните взаимодействовать с ботом, чтобы убедиться, что он работает.

---

## Запуск бота через Docker

Этот бот поддерживает Docker для упрощенного развертывания. Следуйте этим шагам для запуска в контейнере.

### Предварительные требования

Убедитесь, что у вас установлены следующие инструменты:

- Docker
- Docker Compose (необязательно, для поддержки `docker-compose.yml`)

### Сборка и запуск Docker-контейнера

1. Соберите образ Docker:
   ```bash
   docker build -t telegram-bot .
   ```

2. Запустите контейнер:
   ```bash
   docker run --env-file .env -d --name telegram-bot telegram-bot
   ```

### Использование Docker Compose (необязательно)

1. Создайте файл `docker-compose.yml` (если он не предоставлен):

   ```yaml
   version: '3.8'

   services:
     telegram-bot:
       build: .
       container_name: telegram_bot
       restart: always
       env_file:
         - .env
       volumes:
         - .:/app/tg_bot
       command: ["./run.sh"]
   ```

2. Запустите бота с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

---

## Гайд для пользователей Windows/MacOS

### Windows

1. **Установка Python и pip**:
   - Скачайте и установите [Python](https://www.python.org/downloads/) (выберите последнюю версию).
   - Во время установки убедитесь, что включена опция "Add Python to PATH".

2. **Создание виртуального окружения**:
   - Откройте командную строку (Windows PowerShell или CMD).
   - Перейдите в папку с проектом:
     ```bash
     cd путь\до\telegram-bot
     ```
   - Создайте виртуальное окружение:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Запуск бота**:
   ```bash
   python main.py
   ```

### MacOS

1. **Установка Homebrew (если ещё не установлен)**:
   - Выполните команду в терминале:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

2. **Установка Python**:
   - Убедитесь, что Python установлен:
     ```bash
     brew install python
     ```

3. **Создание виртуального окружения**:
   - Перейдите в папку с проектом:
     ```bash
     cd /путь/до/telegram-bot
     ```
   - Создайте виртуальное окружение:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Запуск бота**:
   ```bash
   python main.py
   ```

---

## Устранение неполадок

- **Логи**: Для просмотра логов бота:
  ```bash
  docker logs telegram-bot
  ```

- **Перезапуск**: Если бот вылетел или вы внесли изменения:
  ```bash
  docker restart telegram-bot
  ```

- **Остановка контейнера**:
  ```bash
  docker stop telegram-bot
  ```

---

Для дополнительной информации обратитесь к [документации aiogram](https://docs.aiogram.dev/).
