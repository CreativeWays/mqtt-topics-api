import logging
import sqlite3
from datetime import datetime, timedelta
from threading import RLock, Timer
from typing import Tuple

from .config import BATCH_SIZE, BATCH_TIMEOUT, DB_PATH
from .utils.decode_radiohead_payload import decode_radiohead_payload
from .utils.parse_payload_as_json import parse_payload_as_json
from .utils.serialize_json_payload_as_str import serialize_json_payload_as_str

logger = logging.getLogger(__name__)

radiohead_topic_name = "radiohead"


class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_database()
        # Глобальные переменные для батча
        self.batch_buffer = []
        self.batch_lock = RLock()
        self.batch_timer = None

    def get_connection(self) -> sqlite3.Connection:
        """Создает и возвращает соединение с базой данных"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Это позволяет использовать row['column_name']
        return conn

    def init_database(self):
        """Инициализирует базу данных и создает таблицы"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Создаем таблицу для хранения данных сенсоров
                cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
                )

                # Создаем индекс для быстрого поиска по времени
                cursor.execute(
                    """
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON sensor_data(timestamp)
                """
                )

                conn.commit()
                logger.info("Database initialized successfully")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def insert_sensor_data(self, topic: str, payload: str) -> bool:
        """Вставляет данные сенсора в базу данных"""
        # Подготавливаем запись для батча
        modified_topic = topic
        modified_payload = payload
        if radiohead_topic_name in topic.lower():
            json_payload = parse_payload_as_json(modified_payload)
            json_payload["payload"] = decode_radiohead_payload(
                json_payload.get("payload", [])
            )
            modified_topic = f"{topic}/{json_payload['payload']['sensor_id']}"
            modified_payload = serialize_json_payload_as_str(json_payload)

        record = (modified_topic, modified_payload)
        with self.batch_lock:
            self.batch_buffer.append(record)
            # Проверяем, достигли ли мы размера батча
            if len(self.batch_buffer) >= BATCH_SIZE:
                self.insert_batch()
            elif len(self.batch_buffer) == 1:
                # Если это первое сообщение в батче, запускаем таймер
                self.start_batch_timer()

        return True

    def insert_batch(self) -> bool:
        """Вставляет данные сенсора в базу данных"""
        with self.batch_lock:
            if not self.batch_buffer:
                # Если буфер пуст, сбрасываем таймер и выходим
                self.batch_timer = None
                return False

            current_batch = self.batch_buffer
            self.batch_buffer = []
            # Перезапускаем таймер для следующего батча
            self.batch_timer = None
            self.start_batch_timer()
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(
                    "INSERT INTO sensor_data (topic, payload) VALUES (?, ?)",
                    current_batch,
                )
                conn.commit()
                logger.info(f"Data of len {len(current_batch)} inserted")
                return True

        except sqlite3.Error as e:
            logger.error(f"Error inserting data: {e}")
            # В случае ошибки можно добавить данные обратно в буфер
            with self.batch_lock:
                self.batch_buffer = current_batch + self.batch_buffer
            return False

    # Функция для перезапуска таймера
    def start_batch_timer(self) -> None:
        if self.batch_timer is None:
            logger.info("New Timer started")
            self.batch_timer = Timer(BATCH_TIMEOUT, self.insert_batch)
            self.batch_timer.daemon = True
            self.batch_timer.start()

    def get_recent_data(self, limit: int = 10) -> list:
        """Получает последние записи из базы данных"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, topic, payload, timestamp FROM sensor_data "
                    "ORDER BY timestamp DESC LIMIT ?",
                    (limit,),
                )
                return cursor.fetchall()

        except sqlite3.Error as e:
            logger.error(f"Error fetching data: {e}")
            return []

    def delete_old_records(self, months: int = 3) -> Tuple[int, int]:
        """
        Удаляет записи старше указанного количества месяцев

        Args:
            months: Количество месяцев для хранения данных

        Returns:
            Tuple: (количество удаленных записей, общее количество записей до удаления)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Получаем общее количество записей до удаления
                cursor.execute("SELECT COUNT(*) FROM sensor_data")
                total_before = cursor.fetchone()[0]

                if total_before == 0:
                    logger.info("No records to delete")
                    return 0, 0

                # Вычисляем дату, старше которой удаляем записи
                cutoff_date = (datetime.now() - timedelta(days=months * 30)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # Удаляем старые записи
                cursor.execute(
                    "DELETE FROM sensor_data WHERE timestamp < ?", (cutoff_date,)
                )

                deleted_count = cursor.rowcount
                conn.commit()

                # Получаем количество записей после удаления
                cursor.execute("SELECT COUNT(*) FROM sensor_data")
                total_after = cursor.fetchone()[0]

                logger.info(
                    f"Deleted {deleted_count} records older than {months} months. "
                    f"Total before: {total_before}, after: {total_after}"
                )

                return deleted_count, total_before

        except sqlite3.Error as e:
            logger.error(f"Error deleting old records: {e}")
            return 0, 0

    def get_old_records_count(self, months: int = 3) -> int:
        """
        Возвращает количество записей старше указанного количества месяцев

        Args:
            months: Количество месяцев

        Returns:
            int: Количество старых записей
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cutoff_date = (datetime.now() - timedelta(days=months * 30)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                cursor.execute(
                    "SELECT COUNT(*) FROM sensor_data WHERE timestamp < ?",
                    (cutoff_date,),
                )

                return cursor.fetchone()[0]

        except sqlite3.Error as e:
            logger.error(f"Error counting old records: {e}")
            return 0

    def get_database_stats(self) -> dict:
        """
        Возвращает статистику базы данных

        Returns:
            dict: Статистика БД
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                stats = {}

                # Общее количество записей
                cursor.execute("SELECT COUNT(*) FROM sensor_data")
                stats["total_records"] = cursor.fetchone()[0]

                # Самая старая запись
                cursor.execute("SELECT MIN(timestamp) FROM sensor_data")
                stats["oldest_record"] = cursor.fetchone()[0]

                # Самая новая запись
                cursor.execute("SELECT MAX(timestamp) FROM sensor_data")
                stats["newest_record"] = cursor.fetchone()[0]

                # Количество записей старше 3 месяцев
                stats["records_older_than_3_months"] = self.get_old_records_count(3)

                return stats

        except sqlite3.Error as e:
            logger.error(f"Error getting database stats: {e}")
            return {}

    def get_sensor_data(self, topic: str, limit: int = 10) -> list:
        """Получает последние записи из базы данных"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, topic, payload, timestamp
                    FROM sensor_data
                    WHERE topic = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (topic, limit),
                )
                return cursor.fetchall()

        except sqlite3.Error as e:
            logger.error(f"Error fetching data: {e}")
            return []

    def get_all_topics(self) -> list:
        """Получает последние записи из базы данных"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT DISTINCT topic 
                    FROM sensor_data 
                    ORDER BY topic
                    """,
                )
                return cursor.fetchall()

        except sqlite3.Error as e:
            logger.error(f"Error fetching data: {e}")
            return []
