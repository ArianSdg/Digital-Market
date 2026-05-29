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
    total_supply = Column(Integer, default=0)
    owners = relationship("UserItem", back_populates="item")
    transactions = relationship("Transaction", back_populates="item")

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
    inventory = relationship("UserItem", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class UserItem(Base):
    __tablename__ = 'user_items'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    item_id = Column(Integer, ForeignKey('items.item_id'))
    quantity = Column(Integer, default=0, nullable=False)
    acquired_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="inventory")
    item = relationship("Item", back_populates="owners")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    item_id = Column(Integer, ForeignKey('items.item_id'))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float)
    transaction_type = Column(String)
    transaction_date = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="transactions")
    item = relationship("Item", back_populates="transactions")