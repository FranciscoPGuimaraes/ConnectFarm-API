from collections import defaultdict
from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def calculate_vaccine_coverage(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        vaccine_counts = defaultdict(int)
        total_cows = 0

        for cow in collection.find({"farm_id": farm_id}):
            total_cows += 1
            for vaccine in cow.get("vaccines", []):
                vaccine_type = vaccine.get("type")
                vaccine_counts[vaccine_type] += 1

        vaccine_coverage = {
            vaccine: (count / total_cows) * 100
            for vaccine, count in vaccine_counts.items()
        }

        return {"total_cows": total_cows, "vaccine_coverage": vaccine_coverage}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calculating vaccine coverage: {e}"
        )
