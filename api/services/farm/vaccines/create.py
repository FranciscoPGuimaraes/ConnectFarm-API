from bson import ObjectId
from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo
from api.models.CattleModels import VaccineIn

async def create_vaccine_cattle(farm_id: UUID, cattle_number: int, vaccine: VaccineIn):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        
        vaccine_data = vaccine.dict(by_alias=True, exclude_unset=True)
        vaccine_data["id"] = str(ObjectId())
        
        result = collection.update_one(
            {"farm_id": farm_id, "number": cattle_number},
            {"$push": {"vaccines": vaccine_data}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Cattle not found")
        return {"message": "Vaccine added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding vaccine: {e}")
    finally:
        client.close()
        
        
async def create_vaccine_calf(farm_id: UUID, cattle_number: int, calf_number: int, vaccine: VaccineIn):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        
        vaccine_data = vaccine.dict(by_alias=True, exclude_unset=True)
        vaccine_data["id"] = str(ObjectId())
        
        result = collection.update_one(
            {"farm_id": farm_id, "number": cattle_number, "calves.number": calf_number},
            {"$push": {"calves.$.vaccines": vaccine_data}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Cattle or calf not found")
        return {"message": "Vaccine added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding vaccine: {e}")
    finally:
        client.close()