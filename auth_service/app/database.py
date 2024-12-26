from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Строка подключения к базе данных (обновите под вашу среду)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@postgres/dbname"

# Создание объекта engine для подключения к базе данных (без параметра check_same_thread)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создание базового класса для всех моделей
Base = declarative_base()

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
