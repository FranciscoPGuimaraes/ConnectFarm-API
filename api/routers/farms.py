
from typing import Dict, List
from uuid import UUID
from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user, get_current_user_id
from api.models.FarmModels import FarmIn, FarmOut
from api.services.farm import create_farm, read_farm, read_farms_from_user
from fastapi import APIRouter, Depends

from api.dependencies import get_api_key


router = APIRouter(
    prefix="/farms",
    tags=["Farm"],
    dependencies=[Depends(get_api_key), Security(get_current_user)]
)


@router.post("/create", response_model=Dict,)
async def register_new_user(farm: FarmIn, current_user_id: Dict = Depends(get_current_user_id)) -> Dict:
    try:
        await create_farm(farm, current_user_id)
        return {"message": f"Farm with name {farm.name} created successfully!"}
    except Exception as e:
        raise e
    
    
@router.get("/{farm_id}", response_model=FarmOut)
async def get_farm_by_id(farm_id: str):
    try:
        result = await read_farm(farm_id)
        return result
    except Exception as e:
        raise e
    

@router.get("/", response_model=List[FarmOut])
async def get_farm_by_user(current_user_id: Dict = Depends(get_current_user_id)):
    try:
        print(current_user_id)
        result = await read_farms_from_user(current_user_id)
        return result
    except Exception as e:
        raise e