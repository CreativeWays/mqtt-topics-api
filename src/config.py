import os

from dotenv import find_dotenv, load_dotenv

# Загружаем переменные окружения
load_dotenv(find_dotenv())

# Настройки MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = str(os.getenv("MQTT_USER", ""))
MQTT_PASSWORD = str(os.getenv("MQTT_PASSWORD", ""))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "myapp/sensors/temperature")

# Настройки базы данных
DB_PATH = str(
    os.getenv(
        "DB_PATH",
        os.path.join(os.path.dirname(__file__), "data", "app.db"),
    )
)

# Настройки приложения
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 300))  # Размер пачки
BATCH_TIMEOUT = int(
    os.getenv("BATCH_TIMEOUT", 180.0)
)  # Таймаут в секундах (даже если не набралось BATCH_SIZE)
UNICORN_PORT = int(os.getenv("UNICORN_PORT", 52933))
