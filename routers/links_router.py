from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import get_item_by_link, get_click_count, log_click

router = APIRouter(prefix="/rserv")


@router.get("/{link_id}/clicks")
async def link_click_count(
    link_id: str,
    db: AsyncSession = Depends(get_db),
):
    await get_item_by_link(db, link_id)
    return {"link_id": link_id, "clicks": await get_click_count(db, link_id)}


@router.get("/{link_id}")
async def redirect_link(
    link_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    item = await get_item_by_link(db, link_id)

    # Логируем клик
    await log_click(
        db,
        link_id,
        request.client.host if request.client else None,
        request.headers.get("user-agent")
    )

    # Редирект на оригинальный URL из items
    return RedirectResponse(url=item.description)
