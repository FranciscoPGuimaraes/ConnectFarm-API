from fastapi import FastAPI, HTTPException
from api.services.db import connect_mongo
from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np

app = FastAPI()


# Função para buscar dados dos bezerros no MongoDB
async def get_calf_data(farm_id: str):
    collection, client = connect_mongo("cattles")  # Nome da coleção de gado
    try:
        # Consulta para obter bezerros dentro dos documentos de gado
        pipeline = [
            {"$match": {"farm_id": farm_id}},  # Filtra pelo farm_id
            {"$unwind": "$calves"},  # Desmembrar a lista de bezerros
            {"$unwind": "$calves.weights"},  # Desmembrar a lista de pesos dos bezerros
            {"$sort": {"calves.weights.date": 1}},  # Ordena pesos por data
            {
                "$group": {
                    "_id": {
                        "calf_number": "$calves.number",  # Número do bezerro
                        "mother_number": "$number",  # Número da mãe
                    },
                    "weights": {
                        "$push": {
                            "date": "$calves.weights.date",
                            "weight": "$calves.weights.weight",
                        }
                    },
                }
            },
        ]

        data = list(collection.aggregate(pipeline))

        formatted_data = []
        for calf in data:
            weights = calf["weights"]
            calf_number = calf["_id"]["calf_number"]
            mother_number = calf["_id"]["mother_number"]
            formatted_data.append(
                {
                    "calf_number": calf_number,
                    "mother_number": mother_number,
                    "weights": weights,
                }
            )

        return formatted_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching calf data: {str(e)}"
        )


# Função para calcular a projeção de crescimento e peso futuro de um bezerro
def project_growth(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not data or len(data) < 2:
        return {
            "message": "Not enough data to project growth",
            "predicted_weight": None,
        }

    start_date = datetime.strptime(data[0]["date"], "%Y-%m-%d")
    x = [
        (datetime.strptime(entry["date"], "%Y-%m-%d") - start_date).days
        for entry in data
    ]
    y = [entry["weight"] for entry in data]

    # Calcular a inclinação (m) e o intercepto (b)
    x = np.array(x)
    y = np.array(y)
    m = np.sum((x - np.mean(x)) * (y - np.mean(y))) / np.sum((x - np.mean(x)) ** 2)
    b = np.mean(y) - m * np.mean(x)

    # Função de predição do peso
    def predict_weight(days):
        return m * days + b

    # Projeção para os próximos 6 meses (180 dias)
    future_days = 180
    future_date = start_date + timedelta(days=future_days)
    predicted_weight = predict_weight(future_days)

    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "future_date": future_date.strftime("%Y-%m-%d"),
        "predicted_weight": round(predicted_weight, 2),
    }
