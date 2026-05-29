from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Transaction
from app.schema.transaction import TransactionBase


async def create_transaction(db: AsyncSession, request: TransactionBase):
    try:
        new_transaction = Transaction(
            quantity=request.quantity,
            total_price=request.total_price,
            transaction_type=request.transaction_type
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail='This transaction had been made before')

    db.add(new_transaction)
    await db.refresh(new_transaction)
    return new_transaction

async def get_transaction_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(Transaction).where(Transaction.id == id))
    return result.scalar_one_or_none()

async def get_user_transactions(db: AsyncSession):
    result = await db.execute(select(Transaction))
    return result.all()

async def remove_transaction(db: AsyncSession, id: int):
    transaction = get_transaction_by_id(db, id)
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found')
    await db.delete(transaction)
    return transaction