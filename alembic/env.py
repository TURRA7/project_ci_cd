import asyncio
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.database.FDataBase import Base
from config import DATABASE_TEST_URI

# Создание асинхронного движка
engine = create_async_engine(DATABASE_TEST_URI, poolclass=pool.NullPool)


# Настройка Alembic
def run_migrations_offline():
    context.configure(
        url=DATABASE_TEST_URI,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async with engine.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=Base.metadata,
            )
        )
        await connection.run_sync(lambda _: context.run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
