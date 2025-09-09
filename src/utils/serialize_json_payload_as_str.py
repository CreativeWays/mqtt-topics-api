import json
import logging

from src.config import LOG_LEVEL

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def serialize_json_payload_as_str(payload: dict) -> str:
    json_output = ""
    try:
        json_output = json.dumps(payload)
    except TypeError as e:
        logger.error(f"Error dumping JSON: {e}")
    return json_output
