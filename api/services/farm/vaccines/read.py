from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo

async def read_vaccines_cattle(farm_id: UUID, cattle_number: int):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        result = collection.find_one(
            {"farm_id": farm_id, "number": cattle_number},
            {"vaccines": 1, "_id": 0}
        )
        
        if result is None:
            raise HTTPException(status_code=404, detail="Cattle not found")

        vaccines = result.get("vaccines", [])
        
        return {"vaccines": vaccines}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading vaccines: {e}")
    

async def read_vaccines_calf(farm_id: UUID, cattle_number: int, calf_number: str):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        result = collection.find_one(
            { "farm_id": farm_id, "number": cattle_number, "calves.number": calf_number },
            { "calves.$": 1, "_id": 0 }
        )
        
        if result is None:
            raise HTTPException(status_code=404, detail="Cattle or calf not found")

        calves = result.get("calves", [])
        if not calves:
            raise HTTPException(status_code=404, detail="Calf not found")
        
        calf = next((c for c in calves if c["number"] == calf_number), None)
        if calf is None:
            raise HTTPException(status_code=404, detail="Calf not found")

        vaccines = calf.get("vaccines", [])
        
        return {"vaccines": vaccines}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading vaccines: {e}")
