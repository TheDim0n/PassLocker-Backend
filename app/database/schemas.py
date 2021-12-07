from typing import Optional
from pydantic import BaseModel


# region User
class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id: int

    class Config:
        orm_mode = True

# endregion


# region Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
# endregion


# region Secret
class SecretBase(BaseModel):
    secret: str


class SecretCreate(SecretBase):
    user_id: int


class SecretDB(SecretBase):
    id: int

    class Config:
        orm_mode: True
# endregion
