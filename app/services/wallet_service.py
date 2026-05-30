from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_user

async def increase_balance(db: AsyncSession, user_id: int, amount: float):
    user = await db_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if amount <= 0:
        raise HTTPException(status_code=400, detail='Wrong amount to increase balance')
    user.balance += amount
    await db.flush()
    return user

async def decrease_balance(db: AsyncSession, user_id: int, amount: float):
    user = await db_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if user.balance < amount:
        raise HTTPException(status_code=400, detail='Not enough balance')
    if amount <= 0:
        raise HTTPException(status_code=400, detail='Wrong amount to increase balance')
    user.balance -= amount
    await db.flush()
    return user

async def transfer_balance(db: AsyncSession, from_user_id: int, to_user_id: int, amount: float):
    from_user = await db_user.get_user_by_id(db, from_user_id)
    to_user = await db_user.get_user_by_id(db, to_user_id)
    if not from_user:
        raise HTTPException(status_code=404, detail='User not found')
    if not to_user:
        raise HTTPException(status_code=404, detail='User not found')
    if from_user_id == to_user_id:
        raise HTTPException(status_code=400, detail="Can't transfer item to the same user")

    if from_user.balance < amount:
        raise HTTPException(status_code=400, detail='Not enough balance')
    if amount <= 0:
        raise HTTPException(status_code=400, detail='Wrong amount to increase balance')

    await decrease_balance(db, from_user_id, amount)
    await increase_balance(db, to_user_id, amount)
    return {'Detail: ': f'Transferred from {from_user.username} to {to_user.username} successfully.'}