from typing import List
from fastapi import APIRouter, Depends, Security, HTTPException
from uuid import UUID
from api.models.CattleModels import Calf, CalfIn, CalfUpdate
from api.services.farm.calf import create_calf, update_calf, read_calf, read_calfs
from api.dependencies import get_api_key, get_current_user

router = APIRouter(
    prefix="/farms/{farm_id}/cattles/{cattle_number}/calves",
    tags=["Calf"],
    dependencies=[Depends(get_api_key), Security(get_current_user)]
)

@router.post("/create", description="Create one calf in a cattle")
async def create_calf_endpoint(farm_id: UUID, cattle_number: int, calf: CalfIn):
    try:
        response = await create_calf(farm_id, cattle_number, calf)
        return response
    except Exception as e:
        raise e

@router.put("/{calf_number}", description="Update one calf in a cattle")
async def update_calf_endpoint(farm_id: UUID, cattle_number: int, calf_number: str, update_data: CalfUpdate):
    try:
        response = await update_calf(farm_id, cattle_number, calf_number, update_data)
        return response
    except Exception as e:
        raise e

@router.get("/{calf_number}", description="Get one calf from cattle")
async def read_calf_endpoint(farm_id: UUID, cattle_number: int, calf_number: str):
    try:
        response = await read_calf(farm_id, cattle_number, calf_number)
        return response
    except Exception as e:
        raise e


@router.get("/", description="Get all calves from cattle", response_model=List[Calf])
async def read_calf_endpoint(farm_id: UUID, cattle_number: int):
    try:
        response = await read_calfs(farm_id, cattle_number)
        return response
    except Exception as e:
        raise e