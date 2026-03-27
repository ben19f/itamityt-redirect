from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import get_item_by_link, log_click

router = APIRouter(prefix="/rserv")


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
        request.client.host,
        request.headers.get("user-agent")
    )

    # Редирект на оригинальный URL из items
    return RedirectResponse(url=item.description)