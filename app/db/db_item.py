from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.models import Item
from app.schema.item import ItemBase, ItemUpdate


async def create_item(db: AsyncSession, request: ItemBase):
    try:
        new_item = Item(
            name=request.name,
            default_price=request.default_price,
            dynamic_price=request.dynamic_price,
            craftable=request.craftable,
            total_supply=request.total_supply,
            target_supply=request.target_supply
        )
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=404, detail="Item name already exists.")
    return new_item

async def get_item_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(Item).where(Item.item_id == id))
    return result.scalar_one_or_none()

async def get_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def update_item(db: AsyncSession, id: int, request: ItemBase):
    curr_item = await get_item_by_id(db, id)
    if not curr_item:
        raise HTTPException(status_code=404, detail='Item not found.')

    curr_item.name = request.name
    curr_item.default_price = request.default_price
    curr_item.dynamic_price = request.dynamic_price

    await db.commit()
    await db.refresh(curr_item)
    return curr_item

async def item_update_partial(db: AsyncSession, id: int, request: ItemUpdate):
    curr_item = await get_item_by_id(db, id)
    if not curr_item:
        raise HTTPException(status_code=404, detail='Item not found.')

    if request.name is not None and request.name != "":
        curr_item.name = request.name
    if request.default_price is not None and request.default_price != "":
        curr_item.default_price = request.default_price
    if request.dynamic_price is not None and request.dynamic_price != "":
        curr_item.dynamic_price = request.dynamic_price

    await db.commit()
    await db.refresh(curr_item)
    return curr_item

async def delete_item(db: AsyncSession, id: int):
    curr_item = await get_item_by_id(db, id)
    if not curr_item:
        raise HTTPException(status_code=404, detail='Item not found.')
    await db.delete(curr_item)
    await db.commit()
    return {'message': f'Item "{curr_item.name}" was deleted.'}