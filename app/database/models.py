from sqlalchemy import Column, Integer, ForeignKey, String

from .database import DataBase


class User(DataBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)


class Secret(DataBase):
    __tablename__ = "secret"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
