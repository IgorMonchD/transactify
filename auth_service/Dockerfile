# Базовый образ для Python
FROM python:3.10-slim

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt /app/
COPY alembic /app/auth_service/alembic


# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar -xzv -C /usr/local/bin


# Копирование всех файлов в контейнер
COPY . /app/

# Открытие порта
EXPOSE 8000

# Команда для запуска FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]