from datetime import datetime, timedelta
from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def get_cattle_weights(farm_id: UUID):
    collection, client = connect_mongo("cattles")

    try:
        farm_id_str = str(farm_id)
        six_months_ago = (datetime.utcnow() - timedelta(days=180)).strftime("%Y-%m-%d")

        print(f"Fetching weights for farm ID: {farm_id_str} since {six_months_ago}")

        weights_pipeline = [
            {"$match": {"farm_id": farm_id_str}},
            {"$unwind": "$weights"},
            {"$match": {"weights.date": {"$gte": six_months_ago}}},
            {"$sort": {"weights.date": 1}},
            {
                "$project": {
                    "_id": 0,
                    "number": "$number",
                    "weight": {"$toDouble": "$weights.weight"},
                    "date": "$weights.date",
                }
            },
        ]

        print("Running aggregation pipeline...")
        weights_result = list(collection.aggregate(weights_pipeline))
        print(f"Aggregation result: {weights_result}")

        cattle_data = {}
        for entry in weights_result:
            number = entry["number"]
            if number not in cattle_data:
                cattle_data[number] = {
                    "weights": [],
                    "initial_weight": entry["weight"],
                    "final_weight": entry["weight"],
                    "last_date": entry["date"],
                }
            cattle_data[number]["weights"].append(
                {
                    "date": entry["date"],
                    "weight": entry["weight"],
                }
            )
            if entry["weight"] > cattle_data[number]["final_weight"]:
                cattle_data[number]["final_weight"] = entry["weight"]
                cattle_data[number]["last_date"] = entry["date"]

        # Calcular crescimento e peso previsto
        predicted_weights = []
        for number, data in cattle_data.items():
            growth = data["final_weight"] - data["initial_weight"]
            growth_percentage = (
                (growth / data["initial_weight"]) * 100
                if data["initial_weight"] > 0
                else 0
            )
            avg_daily_growth = growth / 180 if data["weights"] else 0
            days_to_predict = 30  # Dias futuros a serem previstos
            predicted_weight = data["final_weight"] + (
                avg_daily_growth * days_to_predict
            )
            predicted_date = (
                datetime.strptime(data["last_date"], "%Y-%m-%d")
                + timedelta(days=days_to_predict)
            ).strftime("%Y-%m-%d")

            predicted_weights.append(
                {
                    "number": number,
                    "fist_weight": data["initial_weight"],
                    "last_weight": data["final_weight"],
                    "growth_percentage": round(growth_percentage, 2),
                    "predicted_weight": round(predicted_weight, 2),
                    "predicted_date": predicted_date,
                }
            )

        return predicted_weights

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pesos: {e}")
