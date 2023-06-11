from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import main_router
from database import create_tables
import uvicorn
import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT)
