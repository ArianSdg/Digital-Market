from datetime import datetime

from pydantic import BaseModel

class UserItemDisplay(BaseModel):
    user_id: int
    item_id: int
    name: str
    quantity: int
    acquired_at: datetime