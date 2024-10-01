from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import CattleIn


async def create_cattle(farm_id: UUID, cattle: CattleIn):
    collection, client = connect_mongo("cattles")
    try:
        # Convert the model to a dictionary
        cattle_data = cattle.dict(by_alias=True, exclude_unset=True)

        # Ensure weights is a list
        if "weights" in cattle_data:
            if isinstance(cattle_data["weights"], dict):
                cattle_data["weights"] = [cattle_data["weights"]]
            elif not isinstance(cattle_data["weights"], list):
                cattle_data["weights"] = list(cattle_data["weights"])

        # Add the farm_id
        cattle_data["farm_id"] = str(farm_id)

        # Insert the data into MongoDB
        result = collection.insert_one(cattle_data)

        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir dados: {e}")
