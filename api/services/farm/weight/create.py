from datetime import datetime
from fastapi import HTTPException
import requests
from api.services.db import connect_mongo
from api.models.CattleModels import WeightIn


async def create_weight_balance(balanceData: WeightIn):
    collection, client = connect_mongo("cattles")
    try:
        # Data atual no formato "yyyy-mm-dd"
        now = datetime.now().strftime("%Y-%m-%d")

        requests.post(
            "https://connectfarm-localizationsystem-production.up.railway.app/webhook",
            json={"weight": round(10 * balanceData.weight, 2)},
        )

        result = collection.update_one(
            {"identifier": balanceData.identifier},
            {
                "$push": {
                    "weights": {
                        "date": now,
                        "weight": round(10 * balanceData.weight, 2),
                    }
                }
            },
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Cattle not found")
        return {"message": "Weight added successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error adding weight: {e}")
