from uuid import UUID
from fastapi import HTTPException
from api.models.CattleModels import VaccineUpdate
from api.services.db import connect_mongo


async def update_vaccine_cattle(farm_id: UUID, cattle_number: int, vaccine_id: str, vaccine_update: VaccineUpdate):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        update_fields = {f"vaccines.$.{key}": value for key, value in vaccine_update.dict(exclude_unset=True).items()}

        if not update_fields:
            raise HTTPException(status_code=400, detail="No update fields provided")

        result = collection.update_one(
            { "farm_id": farm_id, "number": cattle_number, "vaccines.id": vaccine_id },
            { "$set": update_fields }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Cattle or vaccine not found")

        return {"message": "Vaccine updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating vaccine: {e}")


async def update_vaccine_calf(farm_id: UUID, cattle_number: int, calf_number: str, vaccine_id: str, vaccine_update: VaccineUpdate):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)
        update_fields = {f"calves.$[calf].vaccines.$[vaccine].{key}": value for key, value in vaccine_update.dict(exclude_unset=True).items()}

        if not update_fields:
            raise HTTPException(status_code=400, detail="No update fields provided")

        result = collection.update_one(
            { "farm_id": farm_id, "number": cattle_number, "calves.number": calf_number, "calves.vaccines.id": vaccine_id },
            { "$set": update_fields },
            array_filters=[{"calf.number": calf_number}, {"vaccine.id": vaccine_id}]
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Cattle, calf, or vaccine not found")

        return {"message": "Vaccine updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating vaccine: {e}")