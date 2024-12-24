"""
Конфигурационный файл.

Args:

    * Подключение к основной базе:
    DB_USER: Пользователь PostgreSQL
    DB_PASS: Пароль пользователя PostgreSQL
    DB_HOST: Хост базы данных
    DB_NAME: Название базы данных PostgreSQL

    * Подключение к тестовой базе:
    TEST_DB_USER: Пользователь PostgreSQL
    TEST_DB_PASS: Пароль пользователя PostgreSQL
    TEST_DB_HOST: Хост базы данных
    TEST_DB_NAME: Название базы данных PostgreSQL

Notes:
    Достаёт переменные из окружения.
"""
import os
from dotenv import load_dotenv


load_dotenv()


# Подключение к основной базе данных
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Подключение к тестовой базе данных
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASS = os.environ.get("TEST_DB_PASS")
TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")

DATABASE_TEST_URI = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}/{TEST_DB_NAME}"  # noqa: E501
