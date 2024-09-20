from uuid import UUID

from fastapi import HTTPException
from api.services.db.mongo_connection import connect_mongo


async def get_vaccinations_by_quarter(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    try:
        pipeline = [
            {
                "$match": {
                    "farm_id": str(farm_id)  # Filtra pelo farm_id
                }
            },
            {
                "$unwind": "$vaccines"  # Desfaz a lista de vacinas
            },
            {
                "$addFields": {
                    "vaccines_date": {
                        "$dateFromString": {
                            "dateString": "$vaccines.date",
                            "format": "%d/%m/%Y",  # Especifica o formato da data
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "quadrimester": {
                        "$concat": [
                            {"$toString": {"$year": "$vaccines_date"}},
                            ".",
                            {
                                "$toString": {
                                    "$ceil": {
                                        "$divide": [{"$month": "$vaccines_date"}, 4]
                                    }
                                }
                            },
                        ]
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "quadrimester": "$quadrimester",
                        "vaccine_type": "$vaccines.type",
                    },
                    "total_vaccines": {
                        "$sum": 1
                    },  # Contagem total de vacinas por quadrimestre e tipo
                }
            },
            {
                "$group": {
                    "_id": "$_id.quadrimester",
                    "total_vaccines": {
                        "$sum": "$total_vaccines"
                    },  # Total de vacinas por quadrimestre
                    "vaccine_types": {
                        "$push": {
                            "type": "$_id.vaccine_type",
                            "count": "$total_vaccines",
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "quadrimester": "$_id",
                    "total_vaccines": 1,
                    "vaccine_types": 1,
                }
            },
        ]

        # Executar a pipeline no MongoDB
        results = list(collection.aggregate(pipeline))

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter dados de vacinação: {str(e)}"
        )
