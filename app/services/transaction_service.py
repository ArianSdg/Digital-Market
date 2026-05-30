from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums.transaction_type import TransactionType
from app.db.db_transaction import create_transaction


async def record_transaction(
        db: AsyncSession,
        user_id: int,
        item_id: int,
        quantity: int,
        total_price: float,
        transaction_type: TransactionType
):
    new_transaction = await create_transaction(db, user_id, item_id, quantity, total_price, transaction_type)
    return new_transaction