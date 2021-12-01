from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
