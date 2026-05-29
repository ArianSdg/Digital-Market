from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_item, db_user
from app.db.db_user_item import get_specific_user_item
from app.db.models import UserItem, User


async def add_item_to_user(db: AsyncSession, item_id: int, user_id: int, quantity: int):
    item = await db_item.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    user = await db_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user_item = await get_specific_user_item(db, item_id, user_id)
    if user_item:
        user_item.quantity += quantity
    else:
        user_item = UserItem(
            user_id=user_id,
            item_id=item_id,
            quantity=quantity
        )
        db.add(user_item)

    await db.commit()
    await db.refresh(user_item)
    return user_item

async def decrease_item_quantity_from_user(db: AsyncSession, item_id: int, user_id: int, quantity: int):
    user_item = await get_specific_user_item(db, item_id, user_id)
    if not user_item:
        raise HTTPException(status_code=404, detail='Item not found')
    if user_item.quantity == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This user doesnt have this item')
    if user_item.quantity < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This user does not have this much item')

    user_item.quantity -= quantity
    await db.commit()
    await db.refresh(user_item)
    return user_item

async def read_my_item(db: AsyncSession, item_id: int, user: User):
    user_item = await get_specific_user_item(db, item_id, user.user_id)
    if not user_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return user_item

async def get_user_inventory(db: AsyncSession, user_id: int):
    user = await db_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user.inventory

async def get_user_item_quantity(db: AsyncSession, item_id: int, user_id: int):
    user_item = await get_specific_user_item(db, item_id, user_id)
    if not user_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return user_item.quantity

async def remove_item_from_user(db: AsyncSession, item_id: int, user_id: int):
    user_item = await get_specific_user_item(db, item_id, user_id)
    if not user_item:
        raise HTTPException(status_code=404, detail='Item not found')
    await db.delete(user_item)
    await db.commit()
    return user_item