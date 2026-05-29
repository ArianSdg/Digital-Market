from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from app.router import admin_item, admin_user_item, user, item, admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(item.router)
app.include_router(admin_user.router)
app.include_router(admin_item.router)
app.include_router(admin_user_item.router)

async def create_first_admin():
    pass