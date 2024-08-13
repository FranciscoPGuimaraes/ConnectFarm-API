from http.client import HTTPException
from uuid import UUID
from api.services.db import connect_mongo
from api.models.CattleModels import CalfIn

async def create_calf(farm_id: UUID, cattle_number: int, calf: CalfIn):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        calf_data = calf.dict(by_alias=True, exclude_unset=True)
        
        if "weights" in calf_data and isinstance(calf_data["weights"], dict):
            calf_data["weights"] = [calf_data["weights"]]

        result = collection.update_one(
            {"farm_id": farm_id, "number": cattle_number},
            {"$push": {"calves": calf_data}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Cattle not found")
        return {"message": "Calf added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding calf: {e}")
