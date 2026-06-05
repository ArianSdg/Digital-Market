from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str
    default_price: float
    dynamic_price: float
    craftable: bool
    market_stock: int

class ItemDisplay(BaseModel):
    item_id: int
    name: str
    default_price: float
    dynamic_price: float
    craftable: bool
    market_stock: int
    class Config:
        for_attributes = True

class ItemUpdate(BaseModel):
    name: str | None = Field(None, example='stone')
    default_price: float | None = Field(None, example=100.00)
    dynamic_price: float | None = Field(None, example=100.01)
    craftable: bool | None = Field(None, example=False)