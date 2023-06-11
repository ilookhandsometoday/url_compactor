from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_factory
from config import DOMAIN
from models import Link

main_router = APIRouter()


@main_router.post('/link')
async def add_link(session: AsyncSession = Depends(session_factory)):
    ...


# using POST since this kind of request doesn't really fit the semantics of a DELETE request
@main_router.post('/delete_link')
async def delete_link(session: AsyncSession = Depends(session_factory)):
    ...


@main_router.post('/full_url')
async def full_url(session: AsyncSession = Depends(session_factory)):
    ...


@main_router.get('/{path}')
async def redirect(path: str, session: AsyncSession = Depends(session_factory)):
    ...
