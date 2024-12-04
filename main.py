import uvicorn
from fastapi import FastAPI

from routers.router import router_user


app = FastAPI()
app.include_router(router=router_user)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
