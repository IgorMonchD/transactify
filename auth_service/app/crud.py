from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from .logger import log_action

# Создание пользователя
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        log_action(user, "User fetched")
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        log_action(user, "User fetched by username")
    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, balance=0.0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Логируем создание пользователя
    log_action(db_user, "User created")
    return db_user


def change_password(db: Session, username: str, new_password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        hashed_password = pwd_context.hash(new_password)
        db.query(models.User).filter(models.User.username == username).update({"hashed_password": hashed_password})
        db.commit()

        # Логируем изменение пароля
        log_action(user, "Password changed")