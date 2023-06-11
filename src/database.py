from config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
session_factory = async_sessionmaker(engine)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def session():
    async with session_factory() as session:
        yield session