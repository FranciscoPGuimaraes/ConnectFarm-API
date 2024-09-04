from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Security, HTTPException

from api.dependencies import get_api_key, get_current_user
from api.models.FinancialModels import (
    FinancialTransaction,
    FinancialTransactionIn,
    FinancialTransactionUpdate,
)
from api.services.financial import (
    create_financial,
    update_financial,
    read_financial_by_farm_id,
    delete_financial,
)

router = APIRouter(
    prefix="/farms/{farm_id}/financial",
    tags=["Financial"],
    dependencies=[Depends(get_api_key), Security(get_current_user)],
)


@router.post("/create", description="Create a financial transaction in a farm")
async def create_financial_endpoint(farm_id: UUID, financial: FinancialTransactionIn):
    try:
        _id = await create_financial(farm_id, financial)
        return {"message": f"Financial transaction with id {_id} created successfully!"}
    except Exception as e:
        raise e


@router.put("/{financial_id}", description="Update a financial transaction in a farm")
async def update_financial_endpoint(
    farm_id: UUID, financial_id: UUID, update_data: FinancialTransactionUpdate
):
    try:
        result = await update_financial(farm_id, financial_id, update_data)
        return {
            "message": f"Financial transaction with id {financial_id} updated successfully!",
            "result": result,
        }
    except Exception as e:
        raise e


@router.get(
    "/",
    description="Get all financial transactions for a farm",
    response_model=List[FinancialTransaction],
)
async def read_financial_by_farm_id_endpoint(farm_id: UUID):
    try:
        financial_transactions = await read_financial_by_farm_id(farm_id)
        return financial_transactions
    except Exception as e:
        raise e


@router.delete(
    "/{financial_id}", description="Delete a financial transaction from a farm"
)
async def delete_financial_endpoint(farm_id: UUID, financial_id: UUID):
    try:
        result = await delete_financial(farm_id, financial_id)
        if result:
            return {
                "message": f"Financial transaction with id {financial_id} deleted successfully!"
            }
        else:
            raise HTTPException(
                status_code=404, detail="Financial transaction not found"
            )
    except Exception as e:
        raise e
