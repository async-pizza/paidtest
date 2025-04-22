import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.auth.decorators import auth_wrapper
from apps.common.auth.jwt import JWT
from apps.common.database import get_session
from apps.users.models import User
from apps.users.schema import (
    LoginSchema,
    TokenSchema,
    UserInSchema,
    UserSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/session/", response_model=UserSchema)
async def get_user_session_info(
    current_user: User = Depends(auth_wrapper),
) -> User:
    return current_user


@router.post("/session/auth/")
async def authenticate_user(
    data: LoginSchema, session: AsyncSession = Depends(get_session)
) -> TokenSchema:
    user = await User.first_or_none(session, User.username == data.username)
    if not user or not bcrypt.checkpw(
        data.password.encode(), user.password.encode()
    ):
        raise HTTPException(
            status_code=401, detail="Неверный логин или пароль"
        )
    token = JWT(user.id).create()
    return TokenSchema(token=token)


@router.post("/")
async def create_user(
    data: UserInSchema,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(auth_wrapper),
) -> UserSchema:
    user: User = await User.create(session, **data.model_dump())
    return UserSchema.model_validate(user)
