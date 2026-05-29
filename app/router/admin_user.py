from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.schema.user import UserBase, UserDisplay, UserUpdate
from app.db import db_user
from app.security.auth import get_current_admin

router = APIRouter(prefix='/admin', tags=['Admin perms for users'])

@router.post('/', response_model=UserDisplay)
async def create_user(
        request: UserBase,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_user.create_user(db, request)

@router.get('/user/{id}', response_model=UserDisplay)
async def get_user_by_id(id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = await db_user.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.get('/', response_model=List[UserDisplay])
async def get_users(db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    return await db_user.get_users(db)

@router.put('/user/{id}', response_model=UserDisplay)
async def update_user(
        id: int,
        request: UserBase,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_user.update_user(db, id, request)

@router.patch('/user/{id}', response_model=UserDisplay)
async def update_user_partial(
        id: int,
        request: UserUpdate,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_user.update_user_partial(db, id, request)

@router.delete('/user/{id}')
async def delete_user(id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    return await db_user.delete_user(db, id)