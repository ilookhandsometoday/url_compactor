import uvicorn
import config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import main_router
from database import create_tables
from exception_handlers import attribute_error_handler



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
app.add_exception_handler(AttributeError, attribute_error_handler)

if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT)
