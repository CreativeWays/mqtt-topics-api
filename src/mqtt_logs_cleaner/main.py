#!/usr/bin/env python3
import logging

from shared.database import DatabaseManager

logging.basicConfig(level=logging.INFO)


def main():
    """Ручная очистка старых записей"""
    db_manager = DatabaseManager()

    # Показываем статистику до очистки
    stats = db_manager.get_database_stats()
    print("Database statistics before cleanup:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Подтверждение
    if stats.get("records_older_than_3_months", 0) > 0:
        deleted_count, total_before = db_manager.delete_old_records(3)
        print(f"Deleted {deleted_count} records")

        # Показываем статистику после очистки
        stats_after = db_manager.get_database_stats()
        print("Database statistics after cleanup:")
        for key, value in stats_after.items():
            print(f"  {key}: {value}")
    else:
        print("No records older than 3 months found")


if __name__ == "__main__":
    main()
