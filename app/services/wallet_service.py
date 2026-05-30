from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_user

async def increase_balance(db: AsyncSession, user_id: int, amount: float):
    user = await db_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user.balance += amount
    await db.flush(user)
    return user

async def decrease_balance(db: AsyncSession, user_id: int, amount: float):
    user = await db_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user.balance -= amount
    await db.flush(user)
    return user