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

async def transfer_balance(db: AsyncSession, from_user_id: int, to_user_id: id, amount: float):
    from_user = await db_user.get_user_by_id(db, from_user_id)
    to_user = await db_user.get_user_by_id(db, to_user_id)
    if not from_user:
        raise HTTPException(status_code=404, detail='User not found')
    if not to_user:
        raise HTTPException(status_code=404, detail='User not found')
    from_user -= amount
    to_user += amount
    return {'Detail: ': f'Transferred from {from_user.username} to {to_user.username} successfully.'}