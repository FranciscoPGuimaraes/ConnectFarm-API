from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user
from uuid import UUID

from api.models.CattleModels import VaccineIn, VaccineUpdate
from api.services.farm.vaccines import (
    create_vaccine_cattle,
    create_vaccine_calf,
    read_vaccines_cattle,
    read_vaccines_calf,
    update_vaccine_cattle,
    update_vaccine_calf,
)


router = APIRouter(
    prefix="/farms/{farm_id}/vaccines",
    tags=["Vaccines"],
    dependencies=[Depends(get_api_key), Security(get_current_user)],
)


@router.post(
    "/cattles/{cattle_number}/create", description="Create a vaccine in a cattle"
)
async def create_cattle_endpoint(farm_id: UUID, cattle_number: int, vaccine: VaccineIn):
    try:
        await create_vaccine_cattle(farm_id, cattle_number, vaccine)
        return {"message": "Vaccine created successfully!"}
    except Exception as e:
        raise e


@router.post("/calves/{calf_number}/create", description="Create a vaccine in a calf")
async def create_cattle_endpoint2(
    farm_id: UUID, cattle_number: int, calf_number: str, vaccine: VaccineIn
):
    try:
        await create_vaccine_calf(farm_id, calf_number, vaccine)
        return {"message": "Vaccine created successfully!"}
    except Exception as e:
        raise e


@router.get("/cattles/{cattle_number}/", description="Get vaccines of a cattle")
async def create_cattle_endpoint3(farm_id: UUID, cattle_number: int):
    try:
        vaccines = await read_vaccines_cattle(farm_id, cattle_number)
        return vaccines
    except Exception as e:
        raise e


@router.get("/calves/{calf_number}", description="Get vaccines of a calf")
async def create_cattle_endpoint4(farm_id: UUID, calf_number: str):
    try:
        vaccines = await read_vaccines_calf(farm_id, calf_number)
        return vaccines
    except Exception as e:
        raise e


@router.put(
    "/cattles/{cattle_number}/{vaccine_id}/update",
    description="Update a vaccine in a cattle",
)
async def create_cattle_endpoint5(
    farm_id: UUID, cattle_number: int, vaccine_id: str, vaccine: VaccineUpdate
):
    try:
        await update_vaccine_cattle(farm_id, cattle_number, vaccine_id, vaccine)
        return {"message": "Vaccine updated successfully!"}
    except Exception as e:
        raise e


@router.put(
    "/calves/{calf_number}/{vaccine_id}/update",
    description="Update a vaccine in a calf",
)
async def create_cattle_endpoint6(
    farm_id: UUID,
    cattle_number: int,
    calf_number: str,
    vaccine_id: str,
    vaccine: VaccineUpdate,
):
    try:
        await update_vaccine_calf(
            farm_id, cattle_number, calf_number, vaccine_id, vaccine
        )
        return {"message": "Vaccine updated successfully!"}
    except Exception as e:
        raise e
