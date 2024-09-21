from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def get_locations(farm_id: UUID):
    collection, client = connect_mongo("locations")

    try:
        farm_id_str = str(farm_id)

        # Definir as coordenadas atualizadas das extremidades
        bottom_right = {
            "latitude": -22.26231086486486,
            "longitude": -45.687739110705834,
        }
        top_left = {
            "latitude": -22.256145315315315,
            "longitude": -45.69440112104077,
        }

        # Definir o tamanho do quadrante (ajustável conforme a necessidade)
        quadrant_size = 0.001  # Ajuste para o intervalo desejado

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

        zones_pipeline = [
            {
                "$match": {
                    "farmId": farm_id_str,
                    "latitude": {
                        "$gte": bottom_right["latitude"],
                        "$lte": top_left["latitude"],
                    },
                    "longitude": {
                        "$gte": top_left["longitude"],
                        "$lte": bottom_right["longitude"],
                    },
                }
            },
            {
                "$project": {
                    "latitude_range": {
                        "$floor": {
                            "$divide": [
                                {"$subtract": ["$latitude", bottom_right["latitude"]]},
                                quadrant_size,  # Ajusta o tamanho do quadrante para latitude
                            ]
                        }
                    },
                    "longitude_range": {
                        "$floor": {
                            "$divide": [
                                {"$subtract": ["$longitude", top_left["longitude"]]},
                                quadrant_size,  # Ajusta o tamanho do quadrante para longitude
                            ]
                        }
                    },
                }
            },
            {
                "$group": {
                    "_id": {
                        "latitude_range": "$latitude_range",
                        "longitude_range": "$longitude_range",
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
                            {
                                "$toString": {
                                    "$add": [
                                        bottom_right["latitude"],
                                        {
                                            "$multiply": [
                                                "$_id.latitude_range",
                                                quadrant_size,
                                            ]
                                        },
                                    ]
                                }
                            },
                            "-",
                            {
                                "$toString": {
                                    "$add": [
                                        bottom_right["latitude"],
                                        {
                                            "$multiply": [
                                                {"$add": ["$_id.latitude_range", 1]},
                                                quadrant_size,
                                            ]
                                        },
                                    ]
                                }
                            },
                        ]
                    },
                    "longitude_range": {
                        "$concat": [
                            {
                                "$toString": {
                                    "$add": [
                                        top_left["longitude"],
                                        {
                                            "$multiply": [
                                                "$_id.longitude_range",
                                                quadrant_size,
                                            ]
                                        },
                                    ]
                                }
                            },
                            "-",
                            {
                                "$toString": {
                                    "$add": [
                                        top_left["longitude"],
                                        {
                                            "$multiply": [
                                                {"$add": ["$_id.longitude_range", 1]},
                                                quadrant_size,
                                            ]
                                        },
                                    ]
                                }
                            },
                        ]
                    },
                    "total_count": 1,
                }
            },
        ]

        out_of_bounds_pipeline = [
            {"$match": {"farmId": farm_id_str}},  # Filtra pelo farmId
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
                }
            },
            {
                "$match": {
                    "$or": [
                        {"latitude": {"$lt": bottom_right["latitude"]}},
                        {"latitude": {"$gt": top_left["latitude"]}},
                        {"longitude": {"$lt": top_left["longitude"]}},
                        {"longitude": {"$gt": bottom_right["longitude"]}},
                    ]
                }
            },
            {"$project": {"cowId": 1}},
        ]

        # Execute pipelines
        locations_result = list(collection.aggregate(locations_pipeline))
        zones_result = list(collection.aggregate(zones_pipeline))
        out_of_bounds_cows = list(collection.aggregate(out_of_bounds_pipeline))

        return {
            "locations": locations_result,
            "top_zones": zones_result,
            "out_of_bounds_cows": out_of_bounds_cows,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao analisar dados: {e}")
