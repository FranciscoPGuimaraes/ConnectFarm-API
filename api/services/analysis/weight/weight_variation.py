from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def analyze_weight_variation(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        pipeline = [
            {"$match": {"farm_id": farm_id}},
            {"$unwind": "$weights"},
            {
                "$addFields": {
                    "weights.date": {
                        "$dateFromString": {
                            "dateString": "$weights.date",
                            "format": "%Y-%m-%d",
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "month": {"$month": "$weights.date"},
                        "year": {"$year": "$weights.date"},
                    },
                    "average_weight": {"$avg": "$weights.weight"},
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1}},
            {
                "$project": {
                    "_id": 0,
                    "month": "$_id.month",
                    "year": "$_id.year",
                    "average_weight": 1,
                }
            },
        ]

        weight_data = list(collection.aggregate(pipeline))

        if not weight_data:
            return {"message": "No weight data found for the specified farm_id."}

        return weight_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing weight variation: {e}"
        )
