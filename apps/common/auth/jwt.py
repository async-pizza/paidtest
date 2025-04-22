import logging
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException

from settings import config

logger = logging.getLogger(__name__)


class JWT:
    def __init__(self, user_id: int):
        self.user_id = user_id

    @property
    def payload(self) -> dict[str, int | datetime]:
        return {
            "user_id": self.user_id,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(days=10),
        }

    def create(self) -> str:
        return jwt.encode(self.payload, config.SECRET_KEY, algorithm="HS256")

    @classmethod
    def decode(cls, token: str) -> "JWT":
        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                algorithms=["HS256"],
            )
            return cls(payload["user_id"])
        except jwt.ExpiredSignatureError as e:
            logger.info("Tried to auth with expired token")
            raise HTTPException(
                status_code=401, detail="Действие токена закончилось"
            ) from e
        except jwt.InvalidTokenError as e:
            logger.info("Tried to auth with invalid token")
            raise HTTPException(
                status_code=401, detail="Неверный токен"
            ) from e
