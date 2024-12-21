import asyncio
import uvicorn
import logging
from fastapi import FastAPI

from app.routers.router import router_user
from app.database.FDataBase import create_tables


logging.basicConfig(
    filename="project.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def lifespan(app: FastAPI):
    try:
        # Здесь выполняем асинхронную инициализацию
        await create_tables()
        yield
    except Exception as ex:
        logger.error(f"Error during table creation: {ex}")
        raise

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_user)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
