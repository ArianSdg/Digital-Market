from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums.order_type import OrderStatus, OrderType
from app.db.db_item import get_item_by_id
from app.db.db_market_order import get_order_by_id, create_order
from app.db.models import User, MarketOrder
from app.schema.market_order import MarketOrderCreate
from app.services.inventory_service import get_user_inventory, get_user_item_quantity


async def place_buy_order(db: AsyncSession, request: MarketOrderCreate, user: User):
    item = await get_item_by_id(db, request.item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')

    if request.quantity <= 0 or request.order_price <= 0:
        raise HTTPException(status_code=400, detail='Quantity should be greater than 0')
    if user.balance < request.quantity * request.order_price:
        raise HTTPException(status_code=400, detail='Not enough balance')

    new_order = await create_order(db, request)
    new_order.order_status = OrderStatus.OPEN
    new_order.order_type = OrderType.BUY

    db.add(new_order)
    await db.flush()
    return new_order

async def place_sell_order(db: AsyncSession, request: MarketOrderCreate, user: User):
    item = await get_item_by_id(db, request.item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')

    if request.quantity <= 0 or request.order_price <= 0:
        raise HTTPException(status_code=400, detail='Quantity should be greater than 0')

    user_item_quantity = await get_user_item_quantity(db, item.item_id, user.user_id)
    if user_item_quantity < request.quantity:
        raise HTTPException(status_code=400, detail='Not enough amount of item to sell')

    new_order = await create_order(db, request)
    new_order.order_status = OrderStatus.OPEN
    new_order.order_type = OrderType.SELL

    db.add(new_order)
    await db.flush()
    return new_order

async def cancel_order(db: AsyncSession, id: int):
    order = await get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if order.order_status != OrderStatus.OPEN:
        raise HTTPException(status_code=400, detail='Order is not open')

    order.order_status = OrderStatus.CANCELLED
    return order