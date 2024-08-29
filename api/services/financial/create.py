from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.FinancialModels import FinancialTransaction

async def create_financial(farm_id: UUID, movement: FinancialTransaction):
    collection, client = connect_mongo("financials")
    try:
        movement_data = movement.model_dump(by_alias=True, exclude_unset=True)
        movement_data["farm_id"] = str(farm_id)
        result = collection.insert_one(movement_data)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting data: {e}")

