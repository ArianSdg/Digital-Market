from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserItem

async def get_specific_user_item(db: AsyncSession, item_id: int, user_id: int):
    user_item = await db.execute(
        select(UserItem)
        .where((UserItem.user_id == user_id) & (UserItem.item_id == item_id))
    )
    return user_item.scalar_one_or_none()