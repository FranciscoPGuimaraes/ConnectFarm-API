import os
from uuid import UUID

from fastapi import HTTPException
import requests

from api.services.db.mongo_connection import connect_mongo


cows_status = {}


async def check_out_of_bounds(farm_id: UUID):
    collection, client = connect_mongo("locations")
    try:
        bottom_right = {
            "latitude": -22.26231086486486,
            "longitude": -45.687739110705834,
        }
        top_left = {
            "latitude": -22.256145315315315,
            "longitude": -45.69440112104077,
        }

        out_of_bounds_pipeline = [
            {"$match": {"farmId": str(farm_id)}},
            {"$sort": {"timestamp": -1}},
            {"$group": {"_id": "$cowId", "latest_location": {"$first": "$$ROOT"}}},
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

        out_of_bounds_cows = list(collection.aggregate(out_of_bounds_pipeline))

        # Verificar e enviar notificações
        for cow in out_of_bounds_cows:
            cow_id = cow["cowId"]
            if cow_id not in cows_status or cows_status[cow_id] != "out_of_bounds":
                send_notification(cow_id)
                cows_status[cow_id] = "out_of_bounds"

        # Atualizar estado das vacas que estão dentro do terreno
        for cow_id in cows_status.keys():
            if cow_id not in [cow["cowId"] for cow in out_of_bounds_cows]:
                cows_status[cow_id] = "in_bounds"

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao verificar vacas fora do terreno: {e}"
        )


def send_notification(cattle):
    ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
    ONESIGNAL_REST_API_KEY = os.getenv("ONESIGNAL_REST_API_KEY")

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "contents": {"en": f"A vaca {cattle} saiu do terreno!"},
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}",
    }

    response = requests.post(
        "https://onesignal.com/api/v1/notifications?c=push",
        json=payload,
        headers=headers,
    )
    print("Notificação enviada:", response.json())
