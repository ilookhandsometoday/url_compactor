from config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(DATABASE_URL)
session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def make_session():
    async with session_factory() as session:
        yield session