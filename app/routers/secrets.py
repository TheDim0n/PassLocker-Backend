from fastapi import APIRouter, Depends

from ..database import schemas
from ..utils import auth

router = APIRouter(
    prefix="/secrets",
    tags=["Secrets"]
)


@router.get("/")
async def get_secrets(
    current_user: schemas.UserBase = Depends(auth.get_current_user)
):
    return []
