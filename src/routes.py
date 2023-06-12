import shorten
from fastapi import APIRouter, Depends, Path, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import make_session
from config import DOMAIN
from models import Link
from schemas import LinkRequest
from utils import URL_REGEX

main_router = APIRouter()


@main_router.post('/link')
async def add_link(link: LinkRequest, session: AsyncSession = Depends(make_session)):
    ...


@main_router.delete('/link/{short_url:path}')
async def delete_link(short_url: Annotated[str, Path(description='short link encoded with percent-encoding', regex=URL_REGEX)],
                      session: AsyncSession = Depends(make_session)):
    ...


@main_router.get('/link/')
async def full_url(short_url: Annotated[str, Query(description='short link encoded with percent-encoding', regex=URL_REGEX)],
                   session: AsyncSession = Depends(make_session)):
    ...


@main_router.get('/{path}')
async def redirect(path: str, session=Depends(make_session)):
    ...
