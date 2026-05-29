from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_item
from app.db.database import get_db
from app.schema.item import ItemDisplay

router = APIRouter(prefix='/items', tags=['items'])

@router.get('/{id}', response_model=ItemDisplay)
async def get_item_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await db_item.get_item_by_id(db, id)

@router.get('/', response_model=List[ItemDisplay])
async def get_items(db: AsyncSession = Depends(get_db)):
    return await db_item.get_items(db)