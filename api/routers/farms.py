
from fastapi import APIRouter, Depends, Request

from api.dependencies import get_api_key
from api.models.CattleModels import CattleIn
from api.services.farm import create_cattle


router = APIRouter(
    prefix="/farms",
    tags=["Farm"],
    dependencies=[Depends(get_api_key)]
)


@router.post("/cattle/create")
async def create_cattle(cattle: CattleIn):
    try:
        _id = await create_cattle(cattle)
        return {"message": f"Cattle with id {_id} created successfully!"}
    except Exception as e:
        raise e
