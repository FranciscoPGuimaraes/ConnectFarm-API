from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user
from api.services.analysis import (
    calculate_weaned_calves_ratio,
    analyze_health_history,
    analyze_weaning_time,
    calculate_vaccine_coverage,
    analyze_weight_variation,
    analyze_weight_variation_month,
)


router = APIRouter(
    prefix="/data/{farm_id}",
    tags=["Data Analysis"],
    dependencies=[Depends(get_api_key), Security(get_current_user)],
)


@router.get("/health/history")
async def health_history(farm_id: str):
    try:
        result = await analyze_health_history(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/calves/ratio")
async def weaning_ratio(farm_id: str):
    try:
        result = await calculate_weaned_calves_ratio(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/calves/time")
async def weaning_time(farm_id: str):
    try:
        result = await analyze_weaning_time(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/vaccines/coverage")
async def vaccines_coverage(farm_id: str):
    try:
        result = await calculate_vaccine_coverage(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/weight/variation")
async def weight_variation(farm_id: str):
    try:
        result = await analyze_weight_variation(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/weight/variation/month")
async def weight_variation_month(farm_id: str):
    try:
        result = await analyze_weight_variation_month(farm_id)
        return result
    except Exception as e:
        raise e
