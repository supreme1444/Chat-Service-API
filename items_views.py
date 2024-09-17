from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/items",tags = ["Items"])
@router.get("/")
def list_items():
    return ["Items1","Items2",]
@router.get("/items/{item_id}/")
def get_item_by_id(item_id:Annotated[int,Path(ge=1,lt=1_000_000)]):
    summa_id=item_id+ 56
    return {"item":{"id": summa_id,},}
