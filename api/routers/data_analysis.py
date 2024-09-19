from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user
from api.services.analysis import (
    calculate_weaned_calves_ratio,
    analyze_health_history,
    analyze_weaning_time,
    calculate_vaccine_coverage,
    analyze_weight_variation,
    analyze_weight_variation_month,
    analyze_financials_per_cow,
    analyze_financials_current,
    analyze_weight_gain_vs_spending,
    analyze_financials_prediction,
    get_locations,
    get_calf_data,
    project_growth,
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


@router.get("/calves/growth")
async def all_calves_growth(farm_id: str):
    try:
        calves_data = await get_calf_data(farm_id)
        projections = {}

        # Calcula a projeção de crescimento para cada bezerro
        for calf in calves_data:
            calf_number = calf["calf_number"]
            mother_number = calf["mother_number"]
            data = calf["weights"]
            projection = project_growth(data)

            # Adiciona o número da mãe na resposta
            projections[calf_number] = {"mother_number": mother_number, **projection}

        return projections
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


@router.get("/weight/financial")
async def weight_vs_financial(farm_id: str, start_date: str, end_date: str):
    try:
        result = analyze_weight_gain_vs_spending(farm_id, start_date, end_date)
        return result
    except Exception as e:
        raise e


@router.get("/financial/cattles")
async def financial_by_cattle(farm_id: str):
    try:
        result = await analyze_financials_per_cow(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/financial/current")
async def financials_current(farm_id: str):
    try:
        result = await analyze_financials_current(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/financial/predict")
async def financials_predict(farm_id: str):
    try:
        result = await analyze_financials_prediction(farm_id)
        return result
    except Exception as e:
        raise e


@router.get("/location")
async def location_system(farm_id: str):
    try:
        result = await get_locations(farm_id)
        return result
    except Exception as e:
        raise e
