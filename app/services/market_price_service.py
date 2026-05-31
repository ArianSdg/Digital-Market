import math

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_item import get_item_by_id


async def calculate_item_price(db: AsyncSession, item_id):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')

    ratio = item.target_supply / item.total_supply

    new_price = item.default_price * ratio ** (1 / 3)
    min_price = item.default_price * 0.3
    max_price = item.default_price * 3
    new_price = max(min_price, min(new_price, max_price))
    return new_price


