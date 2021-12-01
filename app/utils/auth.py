from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import password as passwd
from ..database import crud, schemas
from ..dependencies import get_settings


ALGORITHM = "HS256"

settings = get_settings()

user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.root_path}/users/token/",
    scheme_name="User"
)


def authenticate_user(db: Session, username: str, password: str):
    user_db = crud.get_user_by_login(db=db, login=username)
    if not user_db:
        return False
    if not passwd.verify(password, user_db.password):
        return False
    return user_db


def create_user_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt
