from fastapi import HTTPException
from uuid import UUID
from api.helpers.getMonthName import get_month_name
from api.services.db import connect_mongo
from datetime import datetime, timedelta


async def analyze_financials_current(farm_id: UUID):
    collection, client = connect_mongo("financials")
    try:
        now = datetime.utcnow()
        current_month = now.month
        current_year = now.year

        start_of_month = datetime(current_year, current_month, 1)
        end_of_month = (start_of_month.replace(day=28) + timedelta(days=4)).replace(
            day=1
        )

        start_of_year = datetime(current_year, 1, 1)
        end_of_year = datetime(current_year + 1, 1, 1)

        start_of_last_month = (start_of_month - timedelta(days=1)).replace(day=1)
        end_of_last_month = start_of_month

        pipeline_month = [
            {
                "$match": {
                    "farm_id": str(farm_id),
                    "date": {
                        "$gte": start_of_month,
                        "$lt": end_of_month,
                    },
                }
            },
            {
                "$group": {
                    "_id": "$transaction_type",
                    "total_amount": {"$sum": "$value"},
                }
            },
            {"$project": {"_id": 0, "transaction_type": "$_id", "total_amount": 1}},
        ]

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
                    "_id": "$transaction_type",
                    "total_amount": {"$sum": "$value"},
                }
            },
            {"$project": {"_id": 0, "transaction_type": "$_id", "total_amount": 1}},
        ]

        pipeline_last_month = [
            {
                "$match": {
                    "farm_id": str(farm_id),
                    "date": {
                        "$gte": start_of_last_month,
                        "$lt": end_of_last_month,
                    },
                }
            },
            {
                "$group": {
                    "_id": "$transaction_type",
                    "total_amount": {"$sum": "$value"},
                }
            },
            {"$project": {"_id": 0, "transaction_type": "$_id", "total_amount": 1}},
        ]

        result_month = list(collection.aggregate(pipeline_month))
        result_year = list(collection.aggregate(pipeline_year))
        result_last_month = list(collection.aggregate(pipeline_last_month))

        def format_result(result):
            formatted = {"total_spent": 0, "total_received": 0}
            for item in result:
                if item["transaction_type"] == "exit":
                    formatted["total_spent"] = round(item["total_amount"], 2)
                elif item["transaction_type"] == "entry":
                    formatted["total_received"] = round(item["total_amount"], 2)
            return formatted

        def calculate_percentage_change(current, previous):
            if previous == 0 and current == 0:
                return 0
            elif previous == 0:
                return 100.0
            elif current == 0:
                return -100.0
            else:
                return round(((current - previous) / previous) * 100, 2)

        formatted_month = format_result(result_month)
        formatted_last_month = format_result(result_last_month)

        spent_change = calculate_percentage_change(
            formatted_month["total_spent"], formatted_last_month["total_spent"]
        )
        received_change = calculate_percentage_change(
            formatted_month["total_received"], formatted_last_month["total_received"]
        )

        formatted_month["spent_change"] = spent_change
        formatted_month["received_change"] = received_change

        return {
            "month": get_month_name(current_month),
            "year": current_year,
            "monthly": formatted_month,
            "yearly": format_result(result_year),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing financials: {str(e)}",
        )
