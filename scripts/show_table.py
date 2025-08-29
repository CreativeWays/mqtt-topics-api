#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import logging

from src.database import DatabaseManager

logging.basicConfig(level=logging.INFO)


def main():
    """Ручная очистка старых записей"""
    db_manager = DatabaseManager()

    # Показываем статистику до очистки
    records = db_manager.get_recent_data()
    # Print the fetched rows
    print("All users:")
    for record in records:
        print(record)


if __name__ == "__main__":
    main()
