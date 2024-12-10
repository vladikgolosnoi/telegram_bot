
# Функция для запуска main.py
run_main() {
    while true; do
        echo "Запускаем main.py..."
        python3 /app/tg_bot/main.py
        echo "main.py завершился. Перезапуск через 5 секунд..."
        sleep 5
    done
}

run_main &

wait
