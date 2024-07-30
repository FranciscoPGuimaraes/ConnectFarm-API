from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import Cattle

async def read_calf(farm_id: UUID, cattle_number: int, number: str):
    collection, client = connect_mongo("cattles")
    try:
        cattle = collection.find_one({"farm_id": farm_id, "number": cattle_number, "calves.number": number}, {"calves.$": 1})
        if not cattle or "calves" not in cattle:
            raise HTTPException(status_code=404, detail="Calf not found")
        return cattle["calves"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler calf: {e}")
    finally:
        client.close()
