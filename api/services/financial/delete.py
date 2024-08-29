from uuid import UUID
import bson
from fastapi import HTTPException
from api.services.db import connect_mongo

async def delete_financial(farm_id: UUID, financial_id: UUID):
    collection, client = connect_mongo("financial")
    try:
        result = collection.delete_one({"_id": bson.ObjectId(str(financial_id)), "farm_id": str(farm_id)})
        if result.deleted_count == 0:
            return False
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting data: {e}")
