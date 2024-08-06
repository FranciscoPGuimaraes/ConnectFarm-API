from typing import Dict
from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user
from uuid import UUID
from fastapi import APIRouter, Depends

from api.dependencies import get_api_key
from api.models.CattleModels import VaccineIn, VaccineUpdate
from api.services.farm.vaccines import ( 
        create_vaccine_cattle,
        create_vaccine_calf,
        read_vaccines_cattle,
        read_vaccines_calf,
        update_vaccine_cattle,
        update_vaccine_calf,
        delete_vaccine_cattle,
        delete_vaccine_calf                        
    )


router = APIRouter(
    prefix="/farms/{farm_id}/cattles/{cattle_number}/vaccines",
    tags=["Vaccines"],
    dependencies=[Depends(get_api_key), Security(get_current_user)]
)


@router.post("/create", description="Create a vaccine in a cattle")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, vaccine: VaccineIn):
    try:
        await create_vaccine_cattle(farm_id, cattle_number, vaccine)
        return {"message": f"Vaccine created successfully!"}
    except Exception as e:
        raise e
    
    
@router.post("/{calf_number}/create", description="Create a vaccine in a calf")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, calf_number: str, vaccine: VaccineIn):
    try:
        await create_vaccine_calf(farm_id, cattle_number, calf_number, vaccine)
        return {"message": f"Vaccine created successfully!"}
    except Exception as e:
        raise e
    

@router.get("/", description="Get vaccines of a cattle")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int):
    try:
        vaccines = await read_vaccines_cattle(farm_id, cattle_number)
        return vaccines
    except Exception as e:
        raise e
    
    
@router.get("/{calf_number}", description="Get vaccines of a calf")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, calf_number: str):
    try:
        vaccines = await read_vaccines_calf(farm_id, cattle_number, calf_number)
        return vaccines
    except Exception as e:
        raise e
    
    
@router.put("/{vaccine_id}/update", description="Update a vaccine in a cattle")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, vaccine_id: str, vaccine: VaccineUpdate):
    try:
        await update_vaccine_cattle(farm_id, cattle_number, vaccine_id, vaccine)
        return {"message": f"Vaccine updated successfully!"}
    except Exception as e:
        raise e


@router.put("/{calf_number}/{vaccine_id}/update", description="Update a vaccine in a calf")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, calf_number: str, vaccine_id: str, vaccine: VaccineUpdate):
    try:
        await update_vaccine_calf(farm_id, cattle_number, calf_number, vaccine_id, vaccine)
        return {"message": f"Vaccine updated successfully!"}
    except Exception as e:
        raise e


@router.delete("/{vaccine_id}/delete", description="Delete a vaccine in a cattle")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, vaccine_id: str):
    try:
        await delete_vaccine_cattle(farm_id, cattle_number, vaccine_id)
        return {"message": f"Vaccine deleted successfully!"}
    except Exception as e:
        raise e
    
    
@router.delete("/{calf_number}/{vaccine_id}/delete", description="Delete a vaccine in a calf")
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, calf_number: str, vaccine_id: str):
    try:
        await delete_vaccine_calf(farm_id, cattle_number, calf_number, vaccine_id)
        return {"message": f"Vaccine deleted successfully!"}
    except Exception as e:
        raise e