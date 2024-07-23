
from fastapi import APIRouter, Depends, Request

from api.dependencies import get_api_key
from api.services.farm import create_cattle


router = APIRouter(
    prefix="/farms",
    tags=["Farm"],
    dependencies=[Depends(get_api_key)]
)


@router.post("/create")
async def create_new_farm(request: Request):
    farm = await create_cattle()
    print(farm)
    return
