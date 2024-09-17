from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def get_locations(farm_id: UUID):
    collection, client = connect_mongo("locations")

    try:
        farm_id_str = str(farm_id)

        # Pipeline para obter a última localização de cada vaca
        locations_pipeline = [
            {
                "$match": {
                    "farmId": farm_id_str  # Filtra pelo farmId
                }
            },
            {
                "$sort": {"timestamp": -1}  # Ordena por timestamp em ordem decrescente
            },
            {
                "$group": {
                    "_id": "$cowId",  # Agrupa por cowId
                    "latest_location": {
                        "$first": "$$ROOT"
                    },  # Pega o primeiro documento após a ordenação
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "cowId": "$_id",
                    "latitude": "$latest_location.latitude",
                    "longitude": "$latest_location.longitude",
                    "timestamp": "$latest_location.timestamp",
                }
            },
        ]

        # Pipeline para calcular as zonas de maior concentração
        zones_pipeline = [
            {
                "$match": {
                    "farmId": farm_id_str  # Filtra pelo farmId
                }
            },
            {
                "$project": {
                    "latitude": {
                        "$floor": {
                            "$divide": [
                                "$latitude",
                                50,
                            ]  # Divide latitude por 50 e arredonda para baixo
                        }
                    },
                    "longitude": {
                        "$floor": {
                            "$divide": [
                                "$longitude",
                                50,
                            ]  # Divide longitude por 50 e arredonda para baixo
                        }
                    },
                }
            },
            {
                "$group": {
                    "_id": {
                        "latitude_range": "$latitude",
                        "longitude_range": "$longitude",
                    },
                    "total_count": {
                        "$sum": 1
                    },  # Conta o número de pontos em cada quadrante
                }
            },
            {
                "$sort": {"total_count": -1}  # Ordena por quantidade de pontos
            },
            {
                "$limit": 3  # Limita a 3 resultados
            },
            {
                "$project": {
                    "_id": 0,
                    "latitude_range": {
                        "$concat": [
                            {"$toString": {"$multiply": ["$_id.latitude_range", 50]}},
                            "-",
                            {
                                "$toString": {
                                    "$add": [
                                        {"$multiply": ["$_id.latitude_range", 50]},
                                        50,
                                    ]
                                }
                            },
                        ]
                    },
                    "longitude_range": {
                        "$concat": [
                            {"$toString": {"$multiply": ["$_id.longitude_range", 50]}},
                            "-",
                            {
                                "$toString": {
                                    "$add": [
                                        {"$multiply": ["$_id.longitude_range", 50]},
                                        50,
                                    ]
                                }
                            },
                        ]
                    },
                    "total_count": 1,
                }
            },
        ]

        # Execute pipelines
        locations_result = list(collection.aggregate(locations_pipeline))
        zones_result = list(collection.aggregate(zones_pipeline))

        return {"locations": locations_result, "top_zones": zones_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao analisar dados: {e}")
