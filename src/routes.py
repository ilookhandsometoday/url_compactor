import shorten
from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import RedirectResponse
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import make_session
from config import DOMAIN
from models import Link
from schemas import LinkRequest
from utils import URL_REGEX
from urllib.parse import unquote

main_router = APIRouter()


@main_router.post('/link')
async def add_link(link: LinkRequest, session: AsyncSession = Depends(make_session)):
    new_link: Link = Link(original_link=link.url)
    session.add(new_link)
    await session.commit()
    new_link_id: int = await new_link.awaitable_attrs.ID
    short_link: str = DOMAIN + '/' + shorten.id_to_path(new_link_id)
    return {'short_link': short_link}


@main_router.delete('/link/{short_url:path}')
async def delete_link(short_url: Annotated[str, Path(description='short link encoded with percent-encoding', regex=URL_REGEX)],
                      session: AsyncSession = Depends(make_session)):
    success: bool = True

    link_id: int = shorten.path_to_id(unquote(short_url).split('/')[-1])
    try:
        link: Optional[Link] = await session.get(Link, link_id)
        # if link is None, session.delete(link) will fail
        await session.delete(link)
        await session.commit()
    except Exception as e:
        success = False
    return {'success': success}

@main_router.get('/link/')
async def full_url(short_url: Annotated[str, Query(description='short link encoded with percent-encoding', regex=URL_REGEX)],
                   session: AsyncSession = Depends(make_session)):
    link_id = shorten.path_to_id(unquote(short_url).split('/')[-1])
    link: Optional[Link] = await session.get(Link, link_id)
    return {'original_link': await link.awaitable_attrs.original_link}

@main_router.get('/{path}')
async def redirect(path: str, session=Depends(make_session)):
    link_id: int = shorten.path_to_id(path)
    link: Optional[Link] = await session.get(Link, link_id)
    original_link = await link.awaitable_attrs.original_link
    return RedirectResponse(original_link)

