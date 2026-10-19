from models import Item, Click
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from fastapi import HTTPException


async def get_item_by_link(db: AsyncSession, link_id: str):
    """Находит Item по link_id"""
    result = await db.execute(select(Item).filter_by(link_id=link_id))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Link not found")
    return item


async def log_click(
    db: AsyncSession,
    link_id: str,
    ip_address: str | None,
    user_agent: str | None,
):
    """Логирует клик на ссылку в таблицу clicks"""
    click = Click(
        link_id=link_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(click)
    await db.commit()
    return click


async def get_click_count(db: AsyncSession, link_id: str) -> int:
    """Возвращает общее число зарегистрированных переходов по ссылке."""
    result = await db.execute(
        select(func.count(Click.id)).where(Click.link_id == link_id)
    )
    return result.scalar_one()
