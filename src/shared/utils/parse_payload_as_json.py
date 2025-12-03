import json
import logging

from shared.config import LOG_LEVEL

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def parse_payload_as_json(payload: str) -> dict:
    data = {}
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except TypeError as e:
        logger.error(f"Error: Input is not a string or bytes-like object: {e}")
    return data
