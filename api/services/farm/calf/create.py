from http.client import HTTPException
from uuid import UUID
from api.services.db import connect_mongo
from api.models import Calf

async def create_calf(farm_id: UUID, cattle_number: int, calf: Calf):
    collection, client = connect_mongo("cattles")
    try:
        result = collection.update_one(
            {"farm_id": farm_id, "number": cattle_number},
            {"$push": {"calves": calf.dict(by_alias=True, exclude_unset=True)}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Cattle not found")
        return {"message": "Calf added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar calf: {e}")
    finally:
        client.close()
