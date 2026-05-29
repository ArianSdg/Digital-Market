from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.schema.user import UserBase, UserUpdate


password_hash = PasswordHash.recommended()

async def create_user(db: AsyncSession, request: UserBase):
    try:
        new_user = User(
            username=request.username,
            email=request.email,
            hashed_password=password_hash.hash(request.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists.")

async def get_user_by_username(db: AsyncSession, username: str):
    user = await db.execute(select(User).where(User.username == username))
    return user.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, id: int):
    user = await db.execute(select(User).where(User.user_id == id))
    return user.scalar_one_or_none()

async def get_users(db: AsyncSession):
    users = await db.execute(select(User))
    return users.scalars().all()

async def update_user(db: AsyncSession, id: int, request: UserBase):
    curr_user = await get_user_by_id(db, id)
    if not curr_user:
        raise HTTPException(status_code=404, detail='User not found.')

    curr_user.username = request.username
    curr_user.email = request.email
    curr_user.hashed_password = password_hash.hash(request.password)

    await db.commit()
    await db.refresh(curr_user)
    return curr_user

async def update_user_partial(db: AsyncSession, user: User, request: UserUpdate):
    if request.username is not None and request.username != "":
        user.username = request.username
    if request.email is not None and request.email != "":
        user.email = request.email
    if request.password is not None and request.password != "":
        user.hashed_password = password_hash.hash(request.password)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, id: int):
    user = await get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found.')
    await db.delete(user)
    await db.commit()
    return {'message': f'User "{user.username}" was deleted.'}