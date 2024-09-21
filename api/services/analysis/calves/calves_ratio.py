from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


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
