import logging

# Настроим базовое логирование
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_action(user, action):
    logger.info(f"User {user.username} (ID: {user.id}) - {action}")
