from models import Item, Click
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException


async def get_item_by_link(db: AsyncSession, link_id: str):
    """Находит Item по link_id"""
    result = await db.execute(select(Item).filter_by(link_id=link_id))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Link not found")
    return item


async def log_click(db: AsyncSession, link_id: str, ip: str, user_agent: str):
    """Логирует клик на ссылку в таблицу clicks"""
    click = Click(link_id=link_id, ip=ip, user_agent=user_agent)
    db.add(click)
    await db.commit()
    return click