from typing import List
from uuid import UUID
import bson
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import Cattle

async def read_cattle(farm_id: UUID, matrix_number: int) -> Cattle:
    collection, client = connect_mongo("cattles")
    try:
        farm_id_str = str(farm_id)
        result = collection.find_one({"farm_id": farm_id_str, "number": matrix_number})
        if result is None:
            raise HTTPException(status_code=404, detail=f"Cattle with number {matrix_number} not found in farm {farm_id}")

        result["_id"] = str(result["_id"])
        if "weights" in result and not isinstance(result["weights"], list):
            result["weights"] = [result["weights"]]
        
        return Cattle(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    finally:
        client.close()
        

async def read_all_cattles(farm_id: UUID) -> Cattle:
    collection, client = connect_mongo("cattles")
    try:
        farm_id_str = str(farm_id)
        result = collection.find({"farm_id": farm_id_str})
        if result is None:
            raise HTTPException(status_code=404, detail=f"Cattles not found in farm {farm_id}")
        
        # result["_id"] = str(result["_id"])
        # if "weights" in result and not isinstance(result["weights"], list):
        #     result["weights"] = [result["weights"]]
        cattle_list = []
        for cattle in result:
            if "_id" in cattle:
                cattle["_id"] = str(cattle["_id"])  # Converte ObjectId para string
            cattle_list.append(cattle)
        return cattle_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    finally:
        client.close()