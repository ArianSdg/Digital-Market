from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_transaction
from app.schema.transaction import TransactionDisplay

router = APIRouter(prefix='/transactions', tags=['Transactions'])

@router.get('/{id}', response_model=TransactionDisplay)
async def get_transaction(db: AsyncSession, id: int):
    return await db_transaction.get_transaction_by_id(db, id)

@router.get('/user/{user_id}', response_model=TransactionDisplay)
async def get_user_transactions(db: AsyncSession, user_id: int):
    return await db_transaction.get_user_transactions(db, user_id)