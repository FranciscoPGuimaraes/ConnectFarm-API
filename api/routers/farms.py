
from uuid import UUID
from fastapi import APIRouter, Depends, Request

from api.dependencies import get_api_key
from api.models.CattleModels import CattleIn, CattleUpdate
from api.services.farm.cattle import create_cattle, update_cattle, read_cattle


router = APIRouter(
    prefix="/farms",
    tags=["Farm"],
    dependencies=[Depends(get_api_key)]
)


@router.post("/cattle/create")
async def create_cattle_endpoint(cattle: CattleIn):
    try:
        _id = await create_cattle(cattle)
        return {"message": f"Cattle with id {_id} created successfully!"}
    except Exception as e:
        raise e
    
@router.put("/cattle/{cattle_number}")
async def update_cattle_endpoint(cattle_number: int, update_data: CattleUpdate):
    try:
        result = await update_cattle(update_data.farm_id, cattle_number, update_data)
        return result
    except Exception as e:
        raise e

@router.get("/cattle/{matrix_number}")
async def read_cattle_endpoint(farm_id: UUID, matrix_number: int):
    try:
        cattle = await read_cattle(farm_id, matrix_number)
        return cattle
    except Exception as e:
        raise e