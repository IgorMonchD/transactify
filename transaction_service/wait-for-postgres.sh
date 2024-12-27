#!/bin/bash

# Делаем попытки подключения к PostgreSQL каждую секунду
until pg_isready -h postgres -U postgres; do
  echo "Waiting for postgres..."
  sleep 1
done

# Задержка в 2 секунды перед запуском приложения
echo "Postgres is ready, waiting 2 more seconds..."
sleep 2

# Запуск основного приложения
exec "$@"
