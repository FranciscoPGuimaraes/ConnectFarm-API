from fastapi import HTTPException
from api.services.db import connect_mongo


async def analyze_weight_variation_by_age(farm_id: str):
    collection, client = connect_mongo("cattles")
    try:
        pipeline = [
            {"$match": {"farm_id": farm_id}},
            {"$unwind": "$weights"},
            {
                "$addFields": {
                    "age_in_months": {
                        "$let": {
                            "vars": {
                                "birth_date": {
                                    "$dateFromString": {"dateString": "$birth_date"}
                                },
                                "measurement_date": {
                                    "$dateFromString": {"dateString": "$weights.date"}
                                },
                            },
                            "in": {
                                "$subtract": [
                                    {
                                        "$divide": [
                                            {
                                                "$subtract": [
                                                    "$$measurement_date",
                                                    "$$birth_date",
                                                ]
                                            },
                                            1000
                                            * 60
                                            * 60
                                            * 24
                                            * 30,  # Número de milissegundos em um mês
                                        ]
                                    },
                                    0.5,  # Ajuste para arredondar para o mês mais próximo
                                ]
                            },
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": {"age_in_months": "$age_in_months"},
                    "average_weight": {"$avg": "$weights.weight"},
                }
            },
            {"$sort": {"_id.age_in_months": 1}},  # Ordenar por idade
        ]

        result = list(collection.aggregate(pipeline))

        # Preparar resultado no formato desejado
        formatted_result = [
            {
                "age_in_months": int(item["_id"]["age_in_months"]),
                "average_weight": item["average_weight"],
            }
            for item in result
        ]

        return formatted_result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing weight variation by age: {str(e)}",
        )
