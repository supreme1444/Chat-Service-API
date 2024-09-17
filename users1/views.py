from fastapi import APIRouter
from users1.schemas import CreateUser

router = APIRouter(prefix="/users", tags=["Users"])
from users1 import crud


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
