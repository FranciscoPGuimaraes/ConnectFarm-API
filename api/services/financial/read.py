from typing import List
from uuid import UUID
from fastapi import HTTPException
from api.services.db import connect_mongo
from api.models.FinancialModels import FinancialTransaction

async def read_financial_by_farm_id(farm_id: UUID) -> List[FinancialTransaction]:
    collection, client = connect_mongo("financials")
    try:
        farm_id_str = str(farm_id)
        result = collection.find({"farm_id": farm_id_str})
        
        if result is None:
            raise HTTPException(status_code=404, detail=f"No financial transactions found for farm {farm_id}")
        
        transactions_list = []
        for transaction in result:
            if "_id" in transaction:
                transaction["_id"] = str(transaction["_id"])
            transactions_list.append(FinancialTransaction(**transaction))
        
        return transactions_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")