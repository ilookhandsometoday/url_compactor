import shorten
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import make_session
from config import DOMAIN
from models import Link
from schemas import AddLinkRequest, UpdateLinkRequest, ShortLinkPath, RedirectPath, ShortLinkResponse, \
    DeleteLinkResponse, FullUrlResponse, UpdateLinkResponse
from utils import path_from_short_url

main_router = APIRouter()


@main_router.patch('/link/{short_url:path}', response_model=UpdateLinkResponse)
async def update_link(link: UpdateLinkRequest, short_url: ShortLinkPath = Depends(ShortLinkPath.depends), session: AsyncSession = Depends(make_session)):
    link_id: int = shorten.path_to_id(path_from_short_url(short_url.short_url))

    success: bool = True
    try:
        update_pending_link: Optional[Link] = await session.get(Link, link_id)
        # If update_pending_link is None, then the error caused by the expression below will be handled by an app-wide
        # exception handler (see exception_handlers.py
        update_pending_link.original_link = link.url
        await session.commit()
    except Exception as e:
        success = False
    return UpdateLinkResponse(success=success)


@main_router.post('/link', response_model=ShortLinkResponse)
async def add_link(link: AddLinkRequest, session: AsyncSession = Depends(make_session)):
    new_link: Link = Link(original_link=link.url)
    session.add(new_link)
    await session.commit()
    new_link_id: int = await new_link.awaitable_attrs.ID
    short_link: str = DOMAIN + '/' + shorten.id_to_path(new_link_id)
    return ShortLinkResponse(short_link=short_link)


@main_router.delete('/link/{short_url:path}', response_model=DeleteLinkResponse)
async def delete_link(short_url: ShortLinkPath = Depends(ShortLinkPath.depends),
                      session: AsyncSession = Depends(make_session)):
    success: bool = True

    link_id: int = shorten.path_to_id(path_from_short_url(short_url.short_url))
    try:
        link: Optional[Link] = await session.get(Link, link_id)
        # if link is None, session.delete(link) will fail, leading to success = False statement
        await session.delete(link)
        await session.commit()
    except Exception as e:
        success = False
    return DeleteLinkResponse(success=success)


@main_router.get('/link/{short_url:path}', response_model=FullUrlResponse)
async def full_url(short_url: ShortLinkPath = Depends(ShortLinkPath.depends),
                   session: AsyncSession = Depends(make_session)):
    link_id: int = shorten.path_to_id(path_from_short_url(short_url.short_url))
    link: Optional[Link] = await session.get(Link, link_id)
    return FullUrlResponse(original_link=await link.awaitable_attrs.original_link)


@main_router.get('/{path}')
async def redirect(path: RedirectPath = Depends(RedirectPath.depends), session=Depends(make_session)):
    link_id: int = shorten.path_to_id(path.path)
    link: Optional[Link] = await session.get(Link, link_id)
    original_link = await link.awaitable_attrs.original_link
    return RedirectResponse(original_link, status_code=301, headers={
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Expires': '0'
    })

