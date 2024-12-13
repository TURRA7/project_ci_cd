"""
Модуль для работы с базой данных.

Models:

    Product: Содержит основную инфу о пользователе:
        id, first_name, last_name, age, salary, email

Func:

    create_tables: Cозданин таблиц
    drop_all_tables: Удаление таблиц
    get_session: Получение асинхронной сессии базы данных
    get_one_user: Получение информации о пользователе
    add_one_user: Добавление пользователя в базу данных
    update_user_info: Обновление информации о пользователе
    delete_one_user: Удаление пользователя из базы данных
"""
import logging
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.orm import (
    DeclarativeBase, sessionmaker)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import (Column, Integer, String, Float, select)

from config import DATABASE_URI


engine = create_async_engine(DATABASE_URI)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
logger = logging.getLogger(__name__)


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

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    salary = Column(Float, nullable=True, default=0.0)
    email = Column(String, nullable=True)


async def create_tables() -> None:
    """Функция создания таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:
    """Функция удаления всех таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncGenerator[AsyncGenerator,
                                          None]:
    """Функция получения асинхронной сессии."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_one_user(user_id: int,
                       session: AsyncSession = Depends(get_session)
                       ) -> dict | str:
    """
    Получение информации о пользователе.

    Args:

        user_id: ID пользователя в базе данных

    Returns:

        Возвращает словарь с информацией о пользователе,
        если пользователь присутствует в базе, иначе строку
        'Пользователя нет в базе!'
    """
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if isinstance(user, User):
        return {"id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "salary": user.salary,
                "email": user.email}
    else:
        logger.info(
            f"Попытка получения несущуствующего пользователя ID: {user_id}")
        return "Пользователя нет в базе!"


async def add_one_user(first_name: str, last_name: str,
                       age: int, salary: float, email: str,
                       session: AsyncSession = Depends(get_session)
                       ) -> dict:
    """
    Добавление пользователя в базу данных.

    Args:

        first_name: Имя пользователя
        last_name: Фамилия пользователя
        age: Количество полных лет пользователя
        salary: Заработная плата пользователя
        email: Электронная почта пользователя
        session: Асинхронная сессия для базы данных.

    Returns:

        Возвращает словарь с ключём 'message' - сообщение об успехе
        или провале операции, а так же 'status_code'.
    """
    user = User(first_name=first_name, last_name=last_name,
                age=age, salary=salary, email=email)
    if (
        isinstance(user, User) and
        user.first_name and user.last_name and user.age and
        user.salary and user.email
    ):
        session.add(user)
        await session.commit()
        return {"message": "Пользователь добавлен!", "status_code": 200}
    else:
        logger.debug(
            "Проблемы с добавлением пользователя, проверить данные!")
        return {
            "message": "Проблемы с добавлением пользователя!",
            "status_code": 422}


async def update_user_info(user_id: int, first_name: str = None,
                           last_name: str = None, age: int = None,
                           salary: float = None, email: str = None,
                           session: AsyncSession = Depends(get_session)
                           ) -> dict:
    """
    Изменение информации о пользователе.

    Args:

        first_name: Имя пользователя
        last_name: Фамилия пользователя
        age: Количество полных лет пользователя
        salary: Заработная плата пользователя
        email: Электронная почта пользователя
        session: Асинхронная сессия для базы данных.

    Returns:

        Возвращает словарь с ключём 'message' - сообщение об успехе
        или провале операции, а так же 'status_code'.
    """
    result = await session.execute(
        select(User).filter_by(id=user_id)
    )
    user = result.scalar_one_or_none()
    if user is not None:
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if age is not None:
            user.age = age
        if salary is not None:
            user.salary = salary
        if email is not None:
            user.email = email
        await session.commit()
        return {"message": f"Данные пользователя с ID: {user_id} изменены!",
                "status_code": 200}
    else:
        logger.info(
            f"Попытка получения несущуствующего пользователя ID: {user_id}")
        return {"message": f"Пользователь с ID: {user_id} не найден!",
                "status_code": 404}


async def delete_one_user(user_id: int,
                          session: AsyncSession = Depends(get_session)
                          ) -> dict:
    """
    Удаление пользователя из базы данных.

    Args:

        user_id: ID пользователя в базе данных
        session: Асинхронная сессия для базы данных.

    Returns:

        Возвращает словарь с ключём 'message' - сообщение об успехе
        или провале операции, а так же 'status_code'.
    """
    result = await session.execute(
        select(User).filter_by(id=user_id)
    )
    user = result.scalar_one_or_none()
    if isinstance(user, User):
        await session.delete(user)
        await session.commit()
        return {"message": f"Пользователь с ID: {user_id} удалён!",
                "status_code": 200}
    else:
        logger.info(
            f"Попытка получения несущуствующего пользователя ID: {user_id}")
        return {"message": f"Пользователь с ID: {user_id} не найден!",
                "status_code": 404}
