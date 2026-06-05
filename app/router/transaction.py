from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_transaction
from app.db.database import get_db
from app.schema.transaction import TransactionDisplay

router = APIRouter(prefix='/transactions', tags=['Transactions'])

@router.get('/{id}', response_model=TransactionDisplay)
async def get_transaction(id: int, db: AsyncSession = Depends(get_db)):
    return await db_transaction.get_transaction_by_id(db, id)

@router.get('/user/{user_id}', response_model=TransactionDisplay)
async def get_user_transactions(user_id: int, db: AsyncSession = Depends(get_db)):
    return await db_transaction.get_user_transactions(db, user_id)