"""
Модуль для работы с базой данных.

Models:

    Product: Содержит основную инфу о пользователе:
        id, first_name, last_name, age, salary, email

Func:
    ...
"""
from typing import AsyncGenerator
from sqlalchemy.orm import (
    DeclarativeBase, sessionmaker)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (Column, Integer, String, Float)

from config import DB_USER, DB_PASS, DB_HOST, DB_NAME


DATABASE_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_async_engine(DATABASE_URI)
AsyncSession = sessionmaker(
    bind=engine,
    class_=AsyncGenerator,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    ...


class User(Base):
    """
    Таблица с общей информацией о пользователе.

    Args:

        id: id пользователя.
        first_name: Имя пользователя
        last_name: Фамилия пользователя
        age: Количество полных лет пользователя
        salary: Заработная плата пользователя
        email: Электронная почта пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    salary = Column(Float, nullable=True, default=0.0)
    email = Column(String, nullable=True)


async def create_tables() -> None:
    """Функция создания таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())


async def drop_all_tables() -> None:
    """Функция удаления всех таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all())


async def get_session() -> AsyncGenerator[AsyncGenerator,
                                          None]:
    """Функция получения асинхронной сессии."""
    async with AsyncSession() as session:
        yield session
