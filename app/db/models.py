from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Float, Boolean

from app.db.database import Base



class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    default_price = Column(Float)
    dynamic_price = Column(Float)
    craftable = Column(Boolean, default=False)
    amount = Column(Integer, default=0)
    owners = relationship("DbUserItems", back_populates="item")

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    inventory = relationship("DbUserItems", back_populates="user")

class UserItem(Base):
    __tablename__ = 'user_items'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    item_id = Column(Integer, ForeignKey('items.item_id'))
    quantity = Column(Integer, default=0)
    acquired_at = Column(DateTime, default=datetime.now)
    user = relationship("DbUser", back_populates="inventory")
    item = relationship("DbItems", back_populates="owners")