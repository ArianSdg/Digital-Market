from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_user
from app.db.models import User


async def get_balance(db: AsyncSession, user: User):
    user = await db_user.get_user_by_id(db, user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user.balance