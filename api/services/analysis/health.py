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

        total_cows = 0

        for cattle in collection.find({"farm_id": farm_id}):
            total_cows += 1
            cattle_number = cattle.get("number")
            health_history = cattle.get("health_history", [])

            for record in health_history:
                disease = record.get("disease")
                status = record.get("status")

                if disease:
                    disease_count[disease] += 1

                if status == "Recovered" and disease:
                    recovery_count[disease] += 1

                disease_per_cattle[cattle_number].append(record)

        result = {
            "total_cows": total_cows,
            "total_diseases": dict(disease_count),
            "recovery_counts": dict(recovery_count),
            "disease_per_cattle": dict(disease_per_cattle),
            "recovery_rate": {
                disease: round(
                    (recovery_count[disease] / disease_count[disease]) * 100, 2
                )
                for disease in disease_count
            },
        }

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao analisar histórico de saúde: {e}"
        )
