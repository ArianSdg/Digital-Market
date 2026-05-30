from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.database import get_db
from app.db.models import User
from app.schema.token import Token
from app.schema.user import UserBase, UserDisplay, UserUpdate
from app.db import db_user_item, db_user
from app.schema.user_item import UserItemDisplay
from app.security.auth import get_current_user, create_access_token, authenticate_user
from app.services import user_service

router = APIRouter(prefix='/user', tags=['users'])

@router.post('/', response_model=UserDisplay)
async def register(request: UserBase, db: AsyncSession = Depends(get_db)):
    return await db_user.create_user(db, request)

@router.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type='bearer')

@router.get('/me', response_model=UserDisplay)
async def get_user(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.get('/me/item/{item_id}', response_model=UserItemDisplay)
async def read_my_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await db_user_item.read_my_item(db, item_id, user)

@router.patch('/me/profile', response_model=UserDisplay)
async def update_user_partial(
        request: UserUpdate,
        curr_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
        ):
    return await db_user.update_user_partial(db, curr_user, request)

@router.get('/me/balance')
async def get_balance(db: AsyncSession = Depends(get_db), curr_user: User = Depends(get_current_user)):
    return await user_service.get_balance(db, curr_user)