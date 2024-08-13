from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import CattleUpdate

async def update_cattle(farm_id: UUID, matrix_number: int, update_data: CattleUpdate):
    collection, client = connect_mongo("cattles")
    try:
        update_fields = update_data.model_dump(exclude_unset=True)
        farm_id_str = str(farm_id)
        query = {"farm_id": farm_id_str, "number": matrix_number}
        
        update_operations = {}
        
        if "weights" in update_fields and update_fields["weights"] is not None:
            weights = update_fields["weights"]
            if not isinstance(weights, list):
                weights = [weights]
            
            existing_document = collection.find_one(query)
            if existing_document and not isinstance(existing_document.get("weights", []), list):
                collection.update_one(
                    query,
                    {"$set": {"weights": []}}
                )
            
            update_operations.setdefault("$push", {}).update({"weights": {"$each": weights}})
        
        if "reproduction" in update_fields and update_fields["reproduction"] is not None:
            reproduction = update_fields["reproduction"]

            if not isinstance(reproduction, list):
                reproduction = [reproduction]
            update_operations.setdefault("$push", {}).update({"reproduction": {"$each": reproduction}})
        
        if "health_history" in update_fields and update_fields["health_history"] is not None:
            health_history = update_fields["health_history"]

            if not isinstance(health_history, list):
                health_history = [health_history]
            update_operations.setdefault("$push", {}).update({"health_history": {"$each": health_history}})
        
        if "number" in update_fields and update_fields["number"] is not None:
            update_operations["$set"] = {"number": update_fields["number"]}
        
        if not update_operations:
            raise HTTPException(status_code=400, detail="No valid fields to update.")
        
        result = collection.update_one(query, update_operations)
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Cattle with number {matrix_number} not found in farm {farm_id_str}")

        return {"message": f"Cattle with number {matrix_number} in farm {farm_id_str} updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {e}")
