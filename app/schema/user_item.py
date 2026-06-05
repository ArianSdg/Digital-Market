from datetime import datetime

from pydantic import BaseModel

from app.schema.item import ItemDisplay


class UserItemDisplay(BaseModel):
    user_id: int
    item: ItemDisplay
    quantity: int
    acquired_at: datetime
    class Config:
        from_attributes = True