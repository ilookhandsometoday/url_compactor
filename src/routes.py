import shorten
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import make_session
from config import DOMAIN
from models import Link
from schemas import AddLinkRequest, ShortLinkPath, RedirectPath, ShortLinkResponse, DeleteLinkResponse, FullUrlResponse

main_router = APIRouter()


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

    link_id: int = shorten.path_to_id(short_url.short_url.split('/')[-1])
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
    link_id = shorten.path_to_id(short_url.short_url.split('/')[-1])
    link: Optional[Link] = await session.get(Link, link_id)
    return FullUrlResponse(original_link=await link.awaitable_attrs.original_link)


@main_router.get('/{path}')
async def redirect(path: RedirectPath = Depends(RedirectPath.depends), session=Depends(make_session)):
    link_id: int = shorten.path_to_id(path.path)
    link: Optional[Link] = await session.get(Link, link_id)
    original_link = await link.awaitable_attrs.original_link
    return RedirectResponse(original_link, status_code=308)

