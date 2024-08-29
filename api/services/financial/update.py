from uuid import UUID
import bson
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.FinancialModels import FinancialTransactionUpdate


async def update_financial(farm_id: UUID, financial_id: UUID, update_data: FinancialTransactionUpdate):
    collection, client = connect_mongo("financial")
    try:
        update_data_dict = update_data.model_dump(by_alias=True, exclude_unset=True)
        result = collection.update_one(
            {"_id": bson.ObjectId(str(financial_id)), "farm_id": str(farm_id)},
            {"$set": update_data_dict}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Financial transaction not found")
        return result.modified_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {e}")
