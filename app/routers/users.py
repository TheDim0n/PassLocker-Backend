from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth
from ..utils import password as passwd


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=201, summary="Create new user account")
async def create_user(
    new_user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    user_db = crud.get_user_by_login(db=db, login=new_user.login)
    if user_db:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user.password = passwd.hash(new_user.password)
    _ = crud.create_user(db=db, new_user=new_user)
    return Response(status_code=201)


@router.post("/token/", response_model=schemas.Token,
             summary="Get access token for user")
async def get_user_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_db = auth.authenticate_user(db=db, username=form_data.username,
                                     password=form_data.password)
    if not user_db:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_user_access_token({"sub": user_db.login})
    return {"access_token": access_token, "token_type": "bearer"}
