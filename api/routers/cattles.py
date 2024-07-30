from typing import Dict
from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user
from uuid import UUID
from fastapi import APIRouter, Depends

from api.dependencies import get_api_key
from api.models.CattleModels import CattleIn, CattleUpdate
from api.services.farm.cattle import create_cattle, update_cattle, read_cattle


router = APIRouter(
    prefix="/farms/{farm_id}/cattles",
    tags=["Cattle"],
    dependencies=[Depends(get_api_key), Security(get_current_user)]
)


@router.post("/create")
async def create_cattle_endpoint(farm_id: UUID, cattle: CattleIn):
    try:
        _id = await create_cattle(farm_id, cattle)
        return {"message": f"Cattle with id {_id} created successfully!"}
    except Exception as e:
        raise e

@router.put("/{cattle_number}")
async def update_cattle_endpoint(farm_id: UUID, cattle_number: int, update_data: CattleUpdate):
    try:
        result = await update_cattle(farm_id, cattle_number, update_data)
        return result
    except Exception as e:
        raise e

@router.get("/{cattle_number}")
async def read_cattle_endpoint(farm_id: UUID, cattle_number: int):
    try:
        cattle = await read_cattle(farm_id, cattle_number)
        return cattle
    except Exception as e:
        raise e
