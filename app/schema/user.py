from datetime import datetime
from pydantic import BaseModel, Field

from app.schema.role import Role


class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    user_id: int
    username: str
    email: str
    role: Role
    is_active: bool
    created_on: datetime
    updated_on: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str | None = Field(None, example="Sam")
    email: str | None = Field(None, example="Sam@gmail.com")
    password: str | None = Field(None, example="A@Hdoes23#9uaR-")