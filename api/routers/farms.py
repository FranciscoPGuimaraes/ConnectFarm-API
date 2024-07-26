
from typing import Dict
from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user, get_current_user_id
from api.models.FarmModels import FarmIn
from api.services.farm import create_farm


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
