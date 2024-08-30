from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo
from datetime import datetime


async def calculate_weaned_calves_ratio(farm_id: UUID):
    collection, client = connect_mongo("cattles")

    try:
        farm_id_str = str(farm_id)

        # Calcula o total de bezerros na fazenda
        total_calves_pipeline = [
            {"$match": {"farm_id": farm_id_str}},
            {"$unwind": "$calves"},
            {"$group": {"_id": None, "total_calves": {"$sum": 1}}},
        ]
        total_calves_result = collection.aggregate(total_calves_pipeline)
        total_calves = next(total_calves_result, {}).get("total_calves", 0)

        # Calcula o total de bezerros desmamados na fazenda
        weaned_calves_pipeline = [
            {"$match": {"farm_id": farm_id_str}},
            {"$unwind": "$calves"},
            {"$match": {"calves.weaning": {"$exists": True}}},
            {"$group": {"_id": None, "weaned_calves_count": {"$sum": 1}}},
        ]
        weaned_calves_result = collection.aggregate(weaned_calves_pipeline)
        weaned_calves_count = next(weaned_calves_result, {}).get(
            "weaned_calves_count", 0
        )

        if total_calves == 0:
            return {"message": "No calves found in the specified farm_id."}

        weaned_ratio = weaned_calves_count / total_calves
        return {
            "total_calves": total_calves,
            "weaned_calves": weaned_calves_count,
            "weaned_ratio": round(weaned_ratio, 2),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calculating weaned calves ratio: {e}"
        )


async def analyze_weaning_time(farm_id: UUID):
    collection, client = connect_mongo("cattles")

    try:
        farm_id = str(farm_id)
        weaning_times = []

        # Consulta para obter todos os bezerros de uma fazenda específica
        pipeline = [
            {"$match": {"farm_id": farm_id}},  # Filtrar vacas pela fazenda
            {"$unwind": "$calves"},  # Desagregar a lista de bezerros
            {
                "$match": {"calves.weaning": {"$exists": True}}
            },  # Filtrar bezerros com 'weaning' preenchido
        ]
        cursor = collection.aggregate(pipeline)

        for cattle in cursor:
            calf = cattle.get("calves")
            birth_date_str = calf.get("birth_date")
            weaning_date_str = calf.get("weaning")

            if birth_date_str and weaning_date_str:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                weaning_date = datetime.strptime(weaning_date_str, "%Y-%m-%d")
                weaning_time = (weaning_date - birth_date).days
                weaning_times.append(weaning_time)

        # Cálculo das métricas de desmame
        if weaning_times:
            average_weaning_time = sum(weaning_times) / len(weaning_times)
            min_weaning_time = min(weaning_times)
            max_weaning_time = max(weaning_times)
        else:
            average_weaning_time = min_weaning_time = max_weaning_time = None

        result = {
            "total_calves_weaned": len(weaning_times),
            "average_weaning_time": round(average_weaning_time, 2),
            "min_weaning_time": min_weaning_time,
            "max_weaning_time": max_weaning_time,
        }

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing weaning time: {e}"
        )


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
