import asyncio
import uvicorn
from fastapi import FastAPI

from routers.router import router_user
from database.FDataBase import create_tables


app = FastAPI()
app.include_router(router=router_user)


async def main() -> None:
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
