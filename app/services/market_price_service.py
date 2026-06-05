from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_item import get_item_by_id


async def calculate_item_price(db: AsyncSession, item_id):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')

    if item.market_stock == 0:
        max_price = item.default_price * 3
        return max_price

    ratio = item.market_stock

    new_price = item.default_price * ratio ** (1 / 3)
    min_price = item.default_price * 0.3
    max_price = item.default_price * 3
    new_price = max(min_price, min(new_price, max_price))
    return new_price

async def update_item_price(db: AsyncSession, item_id: int):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    new_price = await calculate_item_price(db, item_id)
    item.dynamic_price = new_price
    await db.flush()
    return item