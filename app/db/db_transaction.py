from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums.transaction_type import TransactionType
from app.db.db_user import get_user_by_id
from app.db.models import Transaction


async def create_transaction(
        db: AsyncSession,
        user_id: int,
        item_id: int,
        quantity: int,
        total_price: float,
        transaction_type: TransactionType
):
    new_transaction = Transaction(
        user_id=user_id,
        item_id=item_id,
        quantity=quantity,
        total_price=total_price,
        transaction_type=transaction_type
    )
    db.add(new_transaction)
    await db.flush()
    await db.refresh(new_transaction)
    return new_transaction

async def get_transaction_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(Transaction).where(Transaction.id == id))
    return result.scalar_one_or_none()

async def get_user_transactions(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user.transactions

async def remove_transaction(db: AsyncSession, id: int):
    transaction = await get_transaction_by_id(db, id)
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found')
    await db.delete(transaction)
    await db.flush()
    return transaction