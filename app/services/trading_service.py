from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums.transaction_type import TransactionType
from app.db.db_item import get_item_by_id
from app.db.db_user import get_user_by_id
from app.services.inventory_service import add_item_to_user, decrease_item_quantity_from_user
from app.services.transaction_service import record_transaction
from app.services.wallet_service import decrease_balance, increase_balance


async def buy_item(db: AsyncSession, user_id: int, item_id: int, quantity: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    if quantity <= 0:
        raise HTTPException(status_code=400, detail='Quantity must be greater than zero')

    total_price = float(quantity * item.dynamic_price)
    await decrease_balance(db, user_id, total_price)
    await add_item_to_user(db, item_id, user_id, quantity)
    recorded_transaction = await record_transaction(db, user_id, item_id, quantity, total_price, TransactionType.BUY)

    return {'Transaction: ': recorded_transaction}

async def sell_item(db: AsyncSession, user_id: int, item_id: int, quantity: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    if quantity <= 0:
        raise HTTPException(status_code=400, detail='Quantity must be greater than zero')

    total_price = float(quantity * item.dynamic_price)
    await decrease_item_quantity_from_user(db, item_id, user_id, quantity)
    await increase_balance(db, user_id, total_price)
    recorded_transaction = await record_transaction(db, user_id, item_id, quantity, total_price, TransactionType.SELL)

    return {'Transaction: ': recorded_transaction}