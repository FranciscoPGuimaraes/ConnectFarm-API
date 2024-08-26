from collections import defaultdict
from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


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