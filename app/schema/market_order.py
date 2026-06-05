from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums.order_type import OrderType, OrderStatus
from app.schema.item import ItemDisplay
from app.schema.user import UserDisplay


class MarketOrderCreate(BaseModel):
    user_id: int
    item_id: int
    quantity: int = Field(gt=0)
    order_price: float = Field(gt=0)
    order_type: OrderType

class MarketOrderDisplay(BaseModel):
    user: UserDisplay
    item: ItemDisplay
    quantity: int
    remaining_quantity: int
    order_price: float
    order_type: OrderType
    order_status: OrderStatus
    created_at: datetime
    class Config:
        from_attributes = True

class MarketOrderUpdate(BaseModel):
    user_id: int | None = Field(None, example="1")
    item_id: int | None = Field(None, example="1")
    quantity: int | None = Field(None, gt=0, example="10")
    order_price: float | None = Field(None, gt=0, example="100.10")
    order_type: OrderType | Field(None, example="buy")