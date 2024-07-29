from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.CattleModels import CattleUpdate

async def update_cattle(farm_id: UUID, matrix_number: int, update_data: CattleUpdate):
    collection, client = connect_mongo("cattles")
    try:
        update_fields = update_data.model_dump(exclude_unset=True)
        query = {"farm_id": farm_id, "number": matrix_number}
        
        # Processar a atualização de listas
        if "weights" in update_fields and update_fields["weights"] is not None:
            result = collection.update_one(
                query,
                {"$push": {"weights": update_fields["weights"]}}
            )
        if "reproduction" in update_fields and update_fields["reproduction"] is not None:
            result = collection.update_one(
                query,
                {"$push": {"reproduction": update_fields["reproduction"]}}
            )
        if "health_history" in update_fields and update_fields["health_history"] is not None:
            result = collection.update_one(
                query,
                {"$push": {"health_history": update_fields["health_history"]}}
            )
        
        # Atualizar o número se fornecido e não nulo
        if "number" in update_fields and update_fields["number"] is not None:
            result = collection.update_one(
                query,
                {"$set": {"number": update_fields["number"]}}
            )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Matriz com número {matrix_number} não encontrada na fazenda {farm_id}")

        return {"message": f"Matriz com número {matrix_number} na fazenda {farm_id} atualizada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar dados: {e}")
    finally:
        client.close()