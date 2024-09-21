from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def analyze_weight_variation_month(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    try:
        # Pipeline de agregação para calcular o peso médio por mês, independentemente do ano
        pipeline = [
            {"$match": {"farm_id": farm_id}},  # Filtrar por farm_id
            {"$unwind": "$weights"},  # Desestruturar array de weights
            {
                "$group": {
                    "_id": {
                        "month": {
                            "$month": {
                                "$dateFromString": {"dateString": "$weights.date"}
                            }
                        }
                    },
                    "average_weight": {"$avg": "$weights.weight"},
                }
            },
            {"$sort": {"_id.month": 1}},  # Ordenar por mês
        ]

        result = list(collection.aggregate(pipeline))

        # Preparar resultado no formato desejado
        formatted_result = [
            {"month": item["_id"]["month"], "average_weight": item["average_weight"]}
            for item in result
        ]

        return formatted_result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing weight variation by month: {str(e)}",
        )
