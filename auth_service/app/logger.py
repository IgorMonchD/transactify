import os
import logging

# Убедитесь, что папка для логов существует
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настроим базовое логирование
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Указываем путь к файлу логов
file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_action(user, action):
    logger.info(f"User {user.username} (ID: {user.id}) - {action}")