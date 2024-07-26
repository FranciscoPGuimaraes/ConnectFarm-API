from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import CattleIn

async def create_cattle(cattle: CattleIn):
    collection, client = connect_mongo("cattles")
    try:
        cattle_data = cattle.model_dump(by_alias=True, exclude_unset=True)
        result = collection.insert_one(cattle_data)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir dados: {e}")
    finally:
        client.close()

