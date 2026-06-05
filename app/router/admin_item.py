from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_item
from app.db.database import get_db
from app.db.models import User
from app.schema.item import ItemDisplay, ItemBase, ItemUpdate
from app.security.auth import get_current_admin

router = APIRouter(prefix='/admin/item', tags=['Admin perms for items'])

@router.post('/create', response_model=ItemDisplay)
async def create_item(
        request: ItemBase,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_item.create_item(db, request)

@router.get('/{id}', response_model=ItemDisplay)
async def get_item_by_id(id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    return await db_item.get_item_by_id(db, id)

@router.get('/get/all', response_model=List[ItemDisplay])
async def get_items(db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    return await db_item.get_items(db)

@router.put('/item/{id}', response_model=ItemDisplay)
async def update_item(
        id: int,
        request: ItemBase,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_item.update_item(db, id, request)

@router.patch('/patch/{id}', response_model=ItemDisplay)
async def update_item_partial(
        id: int,
        request: ItemUpdate,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    return await db_item.item_update_partial(db, id, request)

@router.delete('/{id}')
async def delete_item(id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    return await db_item.delete_item(db, id)