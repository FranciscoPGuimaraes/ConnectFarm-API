from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import Cattle

async def read_cattle(farm_id: UUID, matrix_number: int) -> Cattle:
    collection, client = connect_mongo("cattles")
    try:
        result = collection.find_one({"farm_id": farm_id, "number": matrix_number})
        if result is None:
            raise HTTPException(status_code=404, detail=f"Cattle with number {matrix_number} not found in farm {farm_id}")
        return Cattle(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    finally:
        client.close()
