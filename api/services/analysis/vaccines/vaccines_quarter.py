from uuid import UUID
from fastapi import HTTPException
from api.services.db.mongo_connection import connect_mongo

PREDEFINED_VACCINE_TYPES = ["Brucelose", "Leucose Bovina", "Pneumonia Bovina", "Virose"]


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

        # Formatar o resultado para incluir os tipos de vacina pré-definidos
        formatted_results = []
        for result in results:
            formatted_result = {
                "quadrimester": result["quadrimester"],
                "total_vaccines": result["total_vaccines"],
                "vaccine_types": {
                    vaccine["type"]: vaccine["count"]
                    for vaccine in result["vaccine_types"]
                },
            }
            formatted_results.append(formatted_result)

        # Adicionar tipos de vacina que não têm registros
        for quadrimester in formatted_results:
            for vaccine_type in PREDEFINED_VACCINE_TYPES:
                if vaccine_type not in quadrimester["vaccine_types"]:
                    quadrimester["vaccine_types"][vaccine_type] = 0

        return {
            "vaccination_data": formatted_results,
            "vaccine_types": PREDEFINED_VACCINE_TYPES,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter dados de vacinação: {str(e)}"
        )
