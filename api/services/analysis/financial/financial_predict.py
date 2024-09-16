from fastapi import HTTPException
from uuid import UUID
from api.helpers.getMonthName import get_month_name
from api.services.db import connect_mongo
from datetime import datetime
import numpy as np


# Função de Regressão Linear Manual
def simple_linear_regression(x: np.ndarray, y: np.ndarray) -> tuple:
    # Verifica se os dados têm tamanho suficiente
    if len(x) < 2 or len(y) < 2:
        return 0.0, 0.0

    x_mean = np.mean(x)
    y_mean = np.mean(y)
    xy_mean = np.mean(x * y)
    x_squared_mean = np.mean(x**2)

    denominator = x_mean**2 - x_squared_mean

    # Evita divisão por zero
    if denominator == 0:
        return 0.0, 0.0

    slope = (x_mean * y_mean - xy_mean) / denominator
    intercept = y_mean - slope * x_mean

    return slope, intercept


# Função de Previsão
def predict(x: float, slope: float, intercept: float) -> float:
    return slope * x + intercept


# Função Principal de Predição
async def analyze_financials_prediction(farm_id: UUID):
    collection, client = connect_mongo("financials")
    try:
        now = datetime.utcnow()
        current_month = now.month
        current_year = now.year

        # Datas no formato "yyyy-mm-dd"
        start_of_year = datetime(current_year, 1, 1).strftime("%Y-%m-%d")
        end_of_year = datetime(current_year + 1, 1, 1).strftime("%Y-%m-%d")

        # Pipeline para obter os dados do ano atual até o mês atual
        pipeline_year = [
            {
                "$match": {
                    "farm_id": str(farm_id),
                    "date": {
                        "$gte": start_of_year,
                        "$lt": end_of_year,
                    },
                }
            },
            {
                "$group": {
                    "_id": {
                        "$substr": ["$date", 5, 2]
                    },  # Extrai o mês da data no formato "yyyy-mm-dd"
                    "total_amount": {"$sum": "$value"},
                    "transaction_type": {"$first": "$transaction_type"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "month": {"$toInt": "$_id"},
                    "total_amount": 1,
                    "transaction_type": 1,
                }
            },
        ]

        result_year = list(collection.aggregate(pipeline_year))

        # Separa os dados de entrada (lucro) e saída (despesas)
        entries = [data for data in result_year if data["transaction_type"] == "entry"]
        exits = [data for data in result_year if data["transaction_type"] == "exit"]

        # Formata os dados para o modelo de regressão
        X_entry = np.array([data["month"] for data in entries]).reshape(-1, 1)
        y_entry = np.array([data["total_amount"] for data in entries])

        X_exit = np.array([data["month"] for data in exits]).reshape(-1, 1)
        y_exit = np.array([data["total_amount"] for data in exits])

        # Cria e treina o modelo de regressão linear para entradas (lucro)
        if entries:
            entry_slope, entry_intercept = simple_linear_regression(
                X_entry.flatten(), y_entry
            )
        else:
            entry_slope, entry_intercept = 0.0, 0.0

        # Cria e treina o modelo de regressão linear para saídas (despesas)
        if exits:
            exit_slope, exit_intercept = simple_linear_regression(
                X_exit.flatten(), y_exit
            )
        else:
            exit_slope, exit_intercept = 0.0, 0.0

        # Prepara o próximo mês para fazer a previsão
        next_month = current_month + 1 if current_month < 12 else 1
        next_month_name = get_month_name(next_month)  # Obtém o nome do próximo mês

        # Realiza a previsão para o próximo mês para entradas (lucro)
        predicted_next_month_entry = predict(next_month, entry_slope, entry_intercept)

        # Realiza a previsão para o próximo mês para saídas (despesas)
        predicted_next_month_exit = predict(next_month, exit_slope, exit_intercept)

        # Calcula a variação em relação ao último mês para entradas (lucro)
        last_month_entry = [
            data["total_amount"]
            for data in entries
            if data["month"] == current_month - 1
        ]
        if last_month_entry:
            last_month_entry_amount = last_month_entry[0]
            entry_variation = round(
                (
                    (predicted_next_month_entry - last_month_entry_amount)
                    / last_month_entry_amount
                )
                * 100,
                2,
            )
        else:
            entry_variation = 0.0

        # Calcula a variação em relação ao último mês para saídas (despesas)
        last_month_exit = [
            data["total_amount"] for data in exits if data["month"] == current_month - 1
        ]
        if last_month_exit:
            last_month_exit_amount = last_month_exit[0]
            exit_variation = round(
                (
                    (predicted_next_month_exit - last_month_exit_amount)
                    / last_month_exit_amount
                )
                * 100,
                2,
            )
        else:
            exit_variation = 0.0

        return {
            "month_name": next_month_name,
            "entry_prediction": round(predicted_next_month_entry, 2),
            "exit_prediction": round(predicted_next_month_exit, 2),
            "entry_variation_percent": entry_variation,
            "exit_variation_percent": exit_variation,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing financials with prediction: {str(e)}",
        )
