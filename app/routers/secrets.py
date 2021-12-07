from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth


router = APIRouter(
    prefix="/secrets",
    tags=["Secrets"]
)


@router.get("/", response_model=List[schemas.SecretDB])
async def get_secrets(
    current_user: schemas.UserBase = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    user_id = crud.get_user_by_login(db=db, login=current_user.login).id
    secrets_db = crud.get_user_secrets(db=db, user_id=user_id)
    return secrets_db


@router.post("/", status_code=201)
async def create_secret(
    new_secret: schemas.SecretBase,
    current_user: schemas.UserBase = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    user_id = crud.get_user_by_login(db=db, login=current_user.login).id
    _ = crud.create_secret(db=db, new_secret=schemas.SecretCreate(
        secret=new_secret.secret,
        user_id=user_id
    ))
    return Response(status_code=201)


@router.delete("/{id}/", status_code=204)
async def delete_secret(
    id: int,
    current_user: schemas.UserBase = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    _ = crud.delete_secret_by_id(db=db, id=id)
    return Response(status_code=204)
