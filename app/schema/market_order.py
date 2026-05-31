from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums.order_type import OrderType, OrderStatus
from app.db.models import User


class MarketOrderCreate(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)
    order_price: float = Field(gt=0)
    order_type: OrderType

class MarketOrderDisplay(BaseModel):
    username: str
    item_name: str
    quantity: int
    remaining_quantity: int
    order_price: float
    order_type: OrderType
    order_status: OrderStatus
    created_at: datetime
    class Config:
        from_attributes = True