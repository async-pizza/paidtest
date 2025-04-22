import bcrypt
from pydantic import BaseModel, Field, model_validator

from apps.schema import DBSchema
from settings import config


class LoginSchema(BaseModel):
    username: str
    password: str = Field(
        min_length=config.PASSWORD_MIN_LENGTH,
    )


class BaseUserSchema(BaseModel):
    username: str


class UserInSchema(BaseUserSchema):
    password: str = Field(min_length=config.PASSWORD_MIN_LENGTH)

    @model_validator(mode="after")
    def check_password(self) -> "UserInSchema":
        self.password = bcrypt.hashpw(
            self.password.encode(), bcrypt.gensalt()
        ).decode()
        return self


class UserSchema(BaseUserSchema, DBSchema):
    pass


class TokenSchema(BaseModel):
    token: str
