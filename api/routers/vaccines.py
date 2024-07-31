from typing import Dict
from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user
from uuid import UUID
from fastapi import APIRouter, Depends

from api.dependencies import get_api_key
from api.models.CattleModels import VaccineIn
from api.services.farm.vaccines import create_vaccine_cattle, create_vaccine_calf, read_vaccines_cattle, read_vaccines_calf


router = APIRouter(
    prefix="/farms/{farm_id}/cattles/{cattle_number}/vaccines",
    tags=["Vaccines"],
    dependencies=[Depends(get_api_key), Security(get_current_user)]
)


@router.post("/create")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, vaccine: VaccineIn):
    try:
        _id = await create_vaccine_cattle(farm_id, cattle_number, vaccine)
        return {"message": f"Vaccine created successfully!"}
    except Exception as e:
        raise e
    
    
@router.post("/{calf_number}/create")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, calf_number: str, vaccine: VaccineIn):
    try:
        _id = await create_vaccine_calf(farm_id, cattle_number, calf_number, vaccine)
        return {"message": f"Vaccine created successfully!"}
    except Exception as e:
        raise e
    

@router.get("/")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int):
    try:
        vaccines = await read_vaccines_cattle(farm_id, cattle_number)
        return vaccines
    except Exception as e:
        raise e
    
    
@router.get("/{calf_number}")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, calf_number: str):
    try:
        vaccines = await read_vaccines_calf(farm_id, cattle_number, calf_number)
        return vaccines
    except Exception as e:
        raise e