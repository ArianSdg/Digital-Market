from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import inventory_service
from app.db import db_user_item
from app.db.database import get_db
from app.db.models import User
from app.schema.user_item import UserItemDisplay
from app.security.auth import get_current_admin

router = APIRouter(prefix='/admin', tags=['User items'])

@router.post('/add/{user_id}/item/{item_id}', response_model=UserItemDisplay)
async def add_item_to_user(
        item_id: int,
        user_id: int,
        quantity: int,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await inventory_service.add_item_to_user(db, item_id, user_id, quantity)

@router.delete('/remove/{user_id}/item/{item_id}', response_model=UserItemDisplay)
async def remove_item_from_user(
        item_id: int,
        user_id: int,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await inventory_service.remove_item_from_user(db, item_id, user_id)

@router.put('/decrease/{user_id}/item/{item_id}')
async def decrease_item_quantity_from_user(
        item_id: int,
        user_id: int,
        quantity: int,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await inventory_service.decrease_item_quantity_from_user(db, item_id, user_id, quantity)

@router.get('/user/{user_id}/item/{item_id}', response_model=UserItemDisplay)
async def get_specific_user_item(
        item_id: int,
        user_id: int,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_user_item.get_specific_user_item(db, item_id, user_id)

@router.get('/user/{user_id}/inventory', response_model=List[UserItemDisplay])
async def get_user_inventory(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await inventory_service.get_user_inventory(db, user_id)

@router.get('/user/{user_id}/item/{item_id}/quantity')
async def get_user_item_quantity(
        item_id: int,
        user_id: int,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await inventory_service.get_user_item_quantity(db, item_id, user_id)