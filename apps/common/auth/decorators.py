from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.database import get_session
from apps.users.models import User

from .jwt import JWT

OAuth2Schema = HTTPBearer()


async def auth_wrapper(
    token: HTTPAuthorizationCredentials = Depends(OAuth2Schema),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    if not await User.all(session):
        return None

    jwt_token = JWT.decode(token.credentials.replace("Bearer ", ""))
    user = await User.get_or_none(session, jwt_token.user_id)
    if not user:
        raise HTTPException(
            status_code=401, detail="Пользователь с таким токеном не найден"
        )
    return user
