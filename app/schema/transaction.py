from datetime import datetime

from pydantic import BaseModel

from app.core.enums.transaction_type import TransactionType


class TransactionBase(BaseModel):
    quantity: int
    total_price: float
    transaction_type: TransactionType

class TransactionDisplay(BaseModel):
    user_id: int
    item_id: int
    quantity: int
    total_price: float
    transaction_type: TransactionType
    transaction_date: datetime
    class Config:
        from_attributes = True