"""
Конфигурационный файл.

Args:
    DB_USER: Пользователь PostgreSQL
    DB_PASS: Пароль пользователя PostgreSQL
    DB_HOST: Хост базы данных
    DB_NAME: Название базы данных PostgreSQL

Notes:
    Достаёт переменные из окружения.
"""
import os
from dotenv import load_dotenv


load_dotenv()


# Подключение к базе данных
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
