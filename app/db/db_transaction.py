from fastapi import HTTPException
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

async def get_transaction_by_id():
    pass

async def get_user_transactions():
    pass

async def remove_transaction():
    pass