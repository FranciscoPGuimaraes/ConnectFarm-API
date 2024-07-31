from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo


async def delete_vaccine_cattle(farm_id: UUID, cattle_number: int, vaccine_id: str):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        result = collection.update_one(
            {
                "farm_id": farm_id,
                "number": cattle_number
            },
            {
                "$pull": {
                    "vaccines": {"id": vaccine_id}
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Cattle or vaccine not found")

        return {"message": "Vaccine deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting vaccine: {e}")
    finally:
        client.close()


async def delete_vaccine_calf(farm_id: UUID, cattle_number: int, calf_number: str, vaccine_id: str):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        result = collection.update_one(
            {
                "farm_id": farm_id,
                "number": cattle_number,
                "calves.number": calf_number
            },
            {
                "$pull": {
                    "calves.$.vaccines": {"id": vaccine_id}
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Cattle, calf, or vaccine not found")

        return {"message": "Vaccine deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting vaccine: {e}")
    finally:
        client.close()