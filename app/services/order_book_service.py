from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums.order_type import OrderType, OrderStatus
from app.db.db_item import get_item_by_id
from app.db.db_market_order import get_order_by_id
from app.db.models import MarketOrder, User


async def place_order(db: AsyncSession, user: User, item_id: int, quantity: int, order_price: float, order_type: OrderType):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    if quantity < 0 or order_price < 0:
        raise HTTPException(status_code=400, detail='Quantity should be greater than 0')

    new_order = MarketOrder(
        user=user.user_id,
        item_id=item_id,
        quantity=quantity,
        order_price=order_price,
        order_type=order_type
    )
    new_order.order_status = OrderStatus.OPEN

    db.add(new_order)
    await db.flush()
    return new_order

async def cancel_order(db: AsyncSession, id: int):
    order = await get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    order.order_status = OrderStatus.CANCELLED
    return order