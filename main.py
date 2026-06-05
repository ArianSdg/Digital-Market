import asyncio

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import engine, Base, AsyncSessionLocal, get_db
from app.db.models import User
from app.router import admin_item, admin_user_item, user, item, admin_user, transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        await create_first_admin(db)

    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

password_hash = PasswordHash.recommended()

app.include_router(user.router)
app.include_router(item.router)
app.include_router(admin_user.router)
app.include_router(admin_item.router)
app.include_router(admin_user_item.router)
app.include_router(transaction.router)

# TODO: create first admin
async def create_first_admin(db: AsyncSession):
    result = await db.execute(select(User).where(User.username == "admin"))
    admin = result.scalar_one_or_none()
    if admin:
        return

    admin = User(
        user_id=0,
        username="admin",
        email="admin@gmail.com",
        hashed_password=password_hash.hash("admin"),
        role="admin",
        is_active=True
    )

    db.add(admin)
    await db.commit()
    print("admin created")