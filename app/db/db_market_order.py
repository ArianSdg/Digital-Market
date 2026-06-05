from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums.order_type import OrderStatus
from app.db.db_user import get_user_by_id
from app.db.models import MarketOrder
from app.schema.market_order import MarketOrderCreate, MarketOrderUpdate


async def create_order(db: AsyncSession, request: MarketOrderCreate):
    new_order = MarketOrder(
        user_id=request.user_id,
        item_id=request.item_id,
        quantity=request.quantity,
        order_price=request.order_price,
        order_type=request.order_type
    )

    db.add(new_order)
    await db.flush()
    return new_order

async def get_open_orders(db: AsyncSession):
    open_orders = await db.execute(select(MarketOrder).where(MarketOrder.order_status == OrderStatus.OPEN))
    return open_orders.all()

async def get_user_orders(db: AsyncSession, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user_orders = await db.execute(select(MarketOrder).where(MarketOrder.user_id == user_id))
    return user_orders.all()

async def get_order_by_id(db: AsyncSession, id):
    order = await db.execute(select(MarketOrder).where(MarketOrder.id == id))
    return order.scalar_one_or_none()

async def delete_order(db: AsyncSession, id: int):
    order = await get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    await db.delete(order)
    await db.flush()
    return order