from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import Calf

async def update_calf(farm_id: UUID, cattle_number: int, number: str, update_data: Calf):
    collection, client = connect_mongo("cattles")
    try:
        calf_path = f"calves.$[elem]"
        update_fields = {f"{calf_path}.{key}": value for key, value in update_data.dict(by_alias=True, exclude_unset=True).items()}

        result = collection.update_one(
            {"farm_id": farm_id, "number": cattle_number, "calves.number": number},
            {"$set": update_fields},
            array_filters=[{"elem.number": number}]
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Calf not found")
        return {"message": "Calf updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar calf: {e}")
    finally:
        client.close()