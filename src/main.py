import logging
import signal
import sys

from .config import LOG_LEVEL
from .mqtt_app import MQTTApp

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Точка входа в приложение"""
    app = MQTTApp()

    # Обработка сигналов для graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Interrupt signal received")
        app.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Запуск приложения
    app.start()


if __name__ == "__main__":
    main()
