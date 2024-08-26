from collections import defaultdict
from typing import Dict, Any, List
from fastapi import HTTPException
from bson import ObjectId
from uuid import UUID
from api.services.db import connect_mongo


# Função de análise de histórico de saúde
async def analyze_health_history(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    
    try:
        farm_id = str(farm_id)
        disease_count = defaultdict(int)
        recovery_count = defaultdict(int)
        disease_per_cattle = defaultdict(list)
        
        # Consulta para obter o histórico de saúde de todas as matrizes de uma fazenda
        for cattle in collection.find({"farm_id": farm_id}):
            cattle_number = cattle.get("number")
            health_history = cattle.get("health_history", [])
            
            for record in health_history:
                disease = record.get("disease")
                status = record.get("status")
                
                # Contar ocorrência de doenças
                disease_count[disease] += 1
                
                # Contar recuperações
                if status == "Recovered":
                    recovery_count[disease] += 1
                
                # Guardar histórico por matriz
                disease_per_cattle[cattle_number].append(record)
        
        # Preparar resultados de análise
        result = {
            "total_diseases": dict(disease_count),
            "recovery_counts": dict(recovery_count),
            "disease_per_cattle": dict(disease_per_cattle),
            "recovery_rate": {
                disease: (recovery_count[disease] / disease_count[disease]) * 100 
                for disease in disease_count
            }
        }
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing health history: {e}")


async def calculate_weaned_calves_ratio(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    
    try:
        farm_id = str(farm_id)
        
        # Contar o número total de vacas para a fazenda específica
        total_cows = collection.count_documents({"farm_id": farm_id})
        
        # Contar o número de bezerros desmamados (calves com campo 'weaning' preenchido)
        pipeline = [
            {"$match": {"farm_id": farm_id}},  # Filtrar vacas pela fazenda
            {"$unwind": "$calves"},            # Desagregar a lista de bezerros
            {"$match": {"calves.weaning": {"$exists": True}}}  # Filtrar bezerros com 'weaning' preenchido
        ]
        weaned_calves_count = collection.aggregate(pipeline)
        weaned_calves_count = sum(1 for _ in weaned_calves_count)

        if total_cows == 0:
            return {"message": "No cows found in the specified farm_id."}
        
        weaned_ratio = weaned_calves_count / total_cows
        return {
            "total_cows": total_cows,
            "weaned_calves": weaned_calves_count,
            "weaned_ratio": weaned_ratio
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating weaned calves ratio: {e}")