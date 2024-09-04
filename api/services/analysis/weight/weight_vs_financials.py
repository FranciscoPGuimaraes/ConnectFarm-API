from fastapi import HTTPException
from uuid import UUID
from typing import List
from api.services.db import connect_mongo


def analyze_weight_gain_vs_spending(farm_id: str, start_date: str, end_date: str):
    collection_cattle, client_cattle = connect_mongo("cattles")
    collection_financials, client_financials = connect_mongo("financials")

    try:
        # Buscar dados financeiros
        financials_cursor = collection_financials.find(
            {"farm_id": str(farm_id), "date": {"$gte": start_date, "$lte": end_date}}
        )
        financials_data = list(financials_cursor)

        if not financials_data:
            return []

        # Processar dados financeiros
        total_spent_by_matriz = {}
        for financial in financials_data:
            transaction_type = financial.get("transaction_type")
            value = financial.get("value", 0)
            matriz_ids = financial.get("matriz_id", [])
            if transaction_type == "exit":
                for matriz_id in matriz_ids:
                    if matriz_id not in total_spent_by_matriz:
                        total_spent_by_matriz[matriz_id] = 0
                    total_spent_by_matriz[matriz_id] += value

        cattle_cursor = collection_cattle.find({"farm_id": str(farm_id)})
        cattle_data = list(cattle_cursor)

        if not cattle_data:
            print("No cattle data found for the given parameters.")
            return []

        results = []
        for cattle in cattle_data:
            cattle_number = str(cattle["number"])
            weights = cattle.get("weights", [])
            if len(weights) < 2:
                continue

            initial_weight = min(w["weight"] for w in weights)
            final_weight = max(w["weight"] for w in weights)
            weight_gain = final_weight - initial_weight

            # Calcular total gasto
            total_spent = 0
            for financial in financials_data:
                if financial["transaction_type"] == "exit":
                    for matriz_id in financial.get("matriz_id", []):
                        if matriz_id in [c["number"] for c in cattle.get("calves", [])]:
                            total_spent += financial.get("value", 0)

            # Adicionar o resultado
            results.append(
                {
                    "cattle_number": cattle_number,
                    "initial_weight": initial_weight,
                    "final_weight": final_weight,
                    "weight_gain": weight_gain,
                    "total_spent": total_spent,
                    "cost_per_kg_gain": total_spent / weight_gain
                    if weight_gain > 0
                    else None,
                }
            )

        print(f"Results: {results}")  # Debugging print

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating cost per kg gain: {str(e)}",
        )
