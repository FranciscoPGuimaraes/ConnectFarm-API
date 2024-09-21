from typing import List
from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import Calf


async def read_calf(farm_id: UUID, number: str):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        cattle = collection.find_one(
            {"farm_id": farm_id, "calves.number": number},
            {
                "number": 1,
                "calves.$": 1,
            },
        )

        if not cattle or "calves" not in cattle:
            raise HTTPException(status_code=404, detail="Calf not found")

        mother_tag = cattle.get("number")
        calf_data = cattle["calves"][0]

        calf_data["mother_tag"] = mother_tag

        return calf_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler calf: {e}")


async def read_calfs(farm_id: UUID, cattle_number: int) -> List[Calf]:
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        cattle = collection.find_one(
            {"farm_id": farm_id, "number": cattle_number}, {"calves": 1}
        )

        if cattle and "calves" in cattle:
            return cattle["calves"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler calfs: {e}")
