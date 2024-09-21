from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo
import requests


async def fetch_precipitation_data():
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": -22.2522,
        "longitude": -45.7033,
        "start_date": "2024-01-01",
        "end_date": "2024-08-31",
        "hourly": "precipitation",
        "timezone": "America/Sao_Paulo",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Aggregate precipitation by month and year
        precipitation_data = {}
        for entry in data["hourly"]["time"]:
            date_str = entry.split("T")[0]
            year, month, _ = date_str.split("-")
            month_year = f"{month}/{year}"

            if month_year not in precipitation_data:
                precipitation_data[month_year] = 0

            # Summing precipitation data
            precipitation_data[month_year] += data["hourly"]["precipitation"][
                data["hourly"]["time"].index(entry)
            ]

        return precipitation_data

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching precipitation data: {e}"
        )


async def analyze_weight_variation(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    try:
        farm_id = str(farm_id)

        # Fetch precipitation data for the relevant year and month range
        precipitation_data = await fetch_precipitation_data()

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

        # Combine weight data with precipitation data
        for item in weight_data:
            month_year = f"{item['month']:02}/{item['year']}"
            item["precipitation"] = round(precipitation_data.get(month_year, 0), 2)

        return weight_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing weight variation: {e}"
        )
