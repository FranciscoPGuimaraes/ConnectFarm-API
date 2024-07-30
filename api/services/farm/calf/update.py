from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import CalfUpdate, Weight

async def update_calf(farm_id: UUID, cattle_number: int, number: str, update_data: CalfUpdate):
    collection, client = connect_mongo("cattles")
    try:
        farm_id_str = str(farm_id)
        update_fields = update_data.model_dump(exclude_unset=True)
        
        update_operations = {}

        if "weights" in update_fields and update_fields["weights"] is not None:
            weight = update_fields["weights"]
            update_operations.setdefault("$push", {}).update({"calves.$[elem].weights": weight})

        if "annotation" in update_fields and update_fields["annotation"] is not None:
            update_operations.setdefault("$set", {}).update({"calves.$[elem].annotation": update_fields["annotation"]})

        if "birth_date" in update_fields and update_fields["birth_date"] is not None:
            update_operations.setdefault("$set", {}).update({"calves.$[elem].birth_date": update_fields["birth_date"]})

        if "weaning" in update_fields and update_fields["weaning"] is not None:
            update_operations.setdefault("$set", {}).update({"calves.$[elem].weaning": update_fields["weaning"]})

        if "health_history" in update_fields and update_fields["health_history"] is not None:
            health_history_entry = update_fields["health_history"]
            update_operations.setdefault("$push", {}).update({"calves.$[elem].health_history": health_history_entry})

        if not update_operations:
            raise HTTPException(status_code=400, detail="No valid fields to update.")

        result = collection.update_one(
            {"farm_id": farm_id_str, "number": cattle_number, "calves.number": number},
            update_operations,
            array_filters=[{"elem.number": number}]
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Calf not found")
        
        return {"message": "Calf updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating calf: {e}")
    finally:
        client.close()
