from fastapi import APIRouter, Depends
from api.dependencies import get_api_key

from api.models.CattleModels import WeightIn
from api.services.farm.weight import create_weight_balance


router = APIRouter(
    prefix="/farms/weight",
    tags=["Weight"],
    dependencies=[Depends(get_api_key)],
)


@router.post("/create", description="Create a weight in a cattle by balance")
async def create_cattle_endpoint(balanceData: WeightIn):
    try:
        await create_weight_balance(balanceData)
        return {"message": "Weight created successfully!"}
    except Exception as e:
        raise e
