import logging
from typing import Any, Callable

import paho.mqtt.client as mqtt

from .config import MQTT_BROKER, MQTT_PASSWORD, MQTT_PORT, MQTT_TOPIC, MQTT_USER

logger = logging.getLogger(__name__)


class MQTTClient:
    def __init__(self, on_message_callback: Callable[[str, str], None]):
        self.client = mqtt.Client()
        self.on_message_callback = on_message_callback
        self.setup_callbacks()

    def setup_callbacks(self):
        """Настраивает callback-функции MQTT клиента"""
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client: mqtt.Client, userdata: Any, flags: Any, rc: int):
        """Callback при подключении к брокеру"""
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            # Подписываемся на топик
            self.client.subscribe(MQTT_TOPIC)
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def _on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
        """Callback при получении сообщения"""
        try:
            payload = msg.payload.decode()
            logger.info(f"Received `{payload}` from `{msg.topic}` topic")
            self.on_message_callback(msg.topic, payload)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_disconnect(self, client: mqtt.Client, userdata: Any, rc: int):
        """Callback при отключении от брокера"""
        logger.info("Disconnected from MQTT Broker")

    def connect(self):
        """Подключается к MQTT брокеру"""
        try:
            logger.info(
                f"Connecting to MQTT Broker: {MQTT_BROKER}:{MQTT_PORT} and user: {MQTT_USER}"
            )
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    def start(self):
        """Запускает цикл обработки сообщений"""
        self.client.loop_start()

    def stop(self):
        """Останавливает клиент"""
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, payload: str):
        """Публикует сообщение в MQTT"""
        result = self.client.publish(topic, payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"Published `{payload}` to `{topic}`")
        else:
            logger.error(f"Failed to publish message: {result}")
