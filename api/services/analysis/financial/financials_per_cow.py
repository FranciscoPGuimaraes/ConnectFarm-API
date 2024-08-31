from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def analyze_financials_per_cow(farm_id: UUID):
    collection, client = connect_mongo("financials")
    try:
        pipeline = [
            {"$match": {"farm_id": str(farm_id)}},
            {"$unwind": "$matriz_id"},
            {
                "$group": {
                    "_id": {"matriz_id": "$matriz_id", "category": "$category"},
                    "total_gasto": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$transaction_type", "exit"]},
                                "$value",
                                0,
                            ]
                        }
                    },
                    "total_recebido": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$transaction_type", "entry"]},
                                "$value",
                                0,
                            ]
                        }
                    },
                }
            },
            {
                "$group": {
                    "_id": "$_id.matriz_id",
                    "total_gasto": {"$sum": "$total_gasto"},
                    "total_recebido": {"$sum": "$total_recebido"},
                    "gastos_por_categoria": {
                        "$push": {"category": "$_id.category", "gasto": "$total_gasto"}
                    },
                    "ganhos_por_categoria": {
                        "$push": {
                            "category": "$_id.category",
                            "amount": "$total_recebido",
                        }
                    },
                }
            },
            {
                "$addFields": {
                    "lucro": {"$subtract": ["$total_recebido", "$total_gasto"]}
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "total_gasto": 1,
                    "total_recebido": 1,
                    "lucro": 1,
                    "gastos_por_categoria": 1,
                    "percentual_gastos_por_categoria": {
                        "$map": {
                            "input": "$gastos_por_categoria",
                            "as": "categoria",
                            "in": {
                                "category": "$$categoria.category",
                                "percentual": {
                                    "$cond": {
                                        "if": {"$gt": ["$total_gasto", 0]},
                                        "then": {
                                            "$multiply": [
                                                {
                                                    "$divide": [
                                                        "$$categoria.gasto",
                                                        "$total_gasto",
                                                    ]
                                                },
                                                100,
                                            ]
                                        },
                                        "else": 0,
                                    }
                                },
                            },
                        }
                    },
                    "percentual_ganhos_por_categoria": {
                        "$map": {
                            "input": "$ganhos_por_categoria",
                            "as": "categoria",
                            "in": {
                                "category": "$$categoria.category",
                                "percentual": {
                                    "$cond": {
                                        "if": {"$gt": ["$total_recebido", 0]},
                                        "then": {
                                            "$multiply": [
                                                {
                                                    "$divide": [
                                                        "$$categoria.amount",
                                                        "$total_recebido",
                                                    ]
                                                },
                                                100,
                                            ]
                                        },
                                        "else": 0,
                                    }
                                },
                            },
                        }
                    },
                }
            },
            {"$sort": {"_id": 1}},
        ]

        result = list(collection.aggregate(pipeline))

        print(result)

        formatted_result = [
            {
                "id": item["_id"],
                "total_spent": item["total_gasto"],
                "total_received": item["total_recebido"],
                "profit": item["lucro"],
                "percentage_spent_by_category": item["percentual_gastos_por_categoria"],
                "percentage_gains_by_category": item["percentual_ganhos_por_categoria"],
            }
            for item in result
        ]

        return formatted_result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing financials per cow: {str(e)}",
        )
