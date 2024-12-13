import asyncio
import uvicorn
import logging
from fastapi import FastAPI

from app.routers.router import router_user
from app.database.FDataBase import create_tables, drop_all_tables


logging.basicConfig(
    filename="project.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(router=router_user)


async def main() -> None:
    try:
        await create_tables()
    except Exception as ex:
        logger.debug(ex)


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
