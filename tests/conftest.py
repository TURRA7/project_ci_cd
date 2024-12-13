import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import DATABASE_TEST_URI
from app.database.FDataBase import Base, get_session, User
from app.main import app


test_engine = create_async_engine(DATABASE_TEST_URI, future=True, echo=True)
test_async_session = sessionmaker(test_engine,
                                  expire_on_commit=False,
                                  class_=AsyncSession)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    """Подготовка базы данных перед тестами."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Фикстура для получения сеанса базы данных."""
    async with test_async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def db_override_get_db(db_session):
    """Переопределяем зависимость get_db для использования тестовой базы."""
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_session] = _get_test_db
    yield
    app.dependency_overrides[get_session] = None


@pytest_asyncio.fixture(scope="function")
async def client(db_override_get_db):
    """Создаём асинхронный тестовый клиент."""
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def add_data_to_db(db_session):
    """Фикстура, добавляет тестовых пользователей."""
    user_1 = User(first_name="Jack", last_name="Niklson", age=37,
                  salary=270000, email="jack_niklson@gmail.com")
    user_2 = User(first_name="Mindi", last_name="Stars", age=22,
                  salary=55000, email="mindi_star@mail.ru")

    db_session.add(user_1)
    db_session.add(user_2)
    await db_session.commit()

    yield db_session

    result = await db_session.execute(select(User))
    users = result.scalars().all()

    for user in users:
        await db_session.delete(user)
    await db_session.commit()
