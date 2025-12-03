import logging
import time

from shared.config import LOG_LEVEL
from shared.database import DatabaseManager

from .mqtt_client import MQTTClient

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class MQTTApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.mqtt_client = MQTTClient(self.on_mqtt_message)
        self.running = False

    def on_mqtt_message(self, topic: str, payload: str):
        """Обработчик входящих MQTT сообщений"""
        try:
            # Сохраняем данные в базу
            success = self.db_manager.insert_sensor_data(topic, payload)
            if success:
                logger.info(f"Saved message from {topic}")

        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    def start(self):
        """Запускает приложение"""
        try:
            self.running = True

            # Подключаемся к MQTT брокеру
            self.mqtt_client.connect()
            self.mqtt_client.start()

            logger.info("Application started. Press Ctrl+C to stop.")

            # Главный цикл
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            self.stop_and_disconnect()

    def stop_and_disconnect(self):
        """Останавливает приложение"""
        self.running = False
        self.mqtt_client.stop_and_disconnect()
        logger.info("Application stopped")
