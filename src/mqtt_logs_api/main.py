import logging
import sys
import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Query

from shared.config import LOG_LEVEL, UNICORN_PORT
from shared.database import DatabaseManager

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

db_manager = DatabaseManager()


# Функции для работы с жизненным циклом приложения
@asynccontextmanager
async def check_database_health(app: FastAPI):
    # Startup: Проверяем подключение к БД
    # Показываем статистику to confirm connection
    db_manager.get_database_stats()
    yield


# Создание FastAPI приложения
app = FastAPI(
    title="Sensor Data API",
    description="API для доступа к данным с IoT датчиков",
    version="1.0.0",
    lifespan=check_database_health,
)


# Эндпоинт 1: Получение данных по topic
@app.get("/api/data")
async def get_sensor_data(
    topic: str = Query(..., description="Topic name", examples=["device/mqtt"]),
    limit: int = Query(
        100, ge=1, le=1000, description="Amount of records", examples=[100]
    ),
) -> List[dict]:
    """
    Получить последние N записей для указанного топика.
    """
    logger.info(f"Request received for topic: '{topic}' with limit: {limit}")

    try:
        rows = db_manager.get_sensor_data(topic, limit)
        # Конвертируем строки Row в обычные dict
        result = [dict(row) for row in rows]
        logger.info(f"Returning {len(result)} records for topic '{topic}'")
        return result

    except Exception as e:
        logger.error(f"Request error in /api/data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Эндпоинт 2: Получение списка всех уникальных топиков
@app.get("/api/topics")
async def get_all_topics() -> dict:
    """
    Получить список всех уникальных топиков, представленных в базе данных.
    """
    logger.info("Request received for all topics")

    try:
        rows = db_manager.get_all_topics()
        # Извлекаем только значения топиков в список
        topics = [row["topic"] for row in rows]
        logger.info(f"Returning {len(topics)} unique topics")
        return {"topics": topics}

    except Exception as e:
        logger.error(f"Request error in /api/topics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Корневой эндпоинт для проверки работы сервера
@app.get("/")
async def root() -> dict:
    return {
        "message": "Sensor Data API is running",
        "endpoints": {
            "get_data": "/api/data?topic=sensor_1&limit=100",
            "get_topics": "/api/topics",
        },
    }


# Запуск сервера (для разработки)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",  # Слушать на всех интерфейсах
        port=UNICORN_PORT,  # Порт по умолчанию для FastAPI
        log_level="info",
    )
