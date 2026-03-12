#!/bin/bash
# entrypoint.sh - Скрипт для запуска миграций и приложения

# Выход при ошибке
set -e

echo "Ожидание готовности базы данных..."

# Простая проверка доступности порта БД через Python
python << END
import socket
import time
import sys

host = "db"
port = 5432
timeout = 30
start_time = time.time()

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            print("База данных доступна!")
            sys.exit(0)
    except (socket.timeout, ConnectionRefusedError):
        if time.time() - start_time > timeout:
            print("Ошибка: Время ожидания базы данных истекло.")
            sys.exit(1)
        print("База данных еще не готова, ожидание...")
        time.sleep(1)
END

echo "Применение миграций БД..."
alembic upgrade head

# Если нужно автоматически заполнять базу при первом запуске,
# можно раскомментировать следующую строку:
# python src/seed.py

echo "Запуск приложения..."
exec "$@"
