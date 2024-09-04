from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class FinancialCategory(str, Enum):
    FEEDING = "feeding"
    PRODUCTION = "production"


class FinancialTransactionIn(BaseModel):
    transaction_type: str
    description: str
    value: float
    date: str
    matriz_id: Optional[List[int]] = None
    category: FinancialCategory


class FinancialTransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    date: Optional[str] = None
    matriz_id: Optional[List[int]] = None
    category: Optional[FinancialCategory] = None


class FinancialTransaction(BaseModel):
    id: str = Field(alias="_id")
    transaction_type: str
    description: str
    value: float
    date: str
    matriz_id: Optional[List[int]] = None
    category: FinancialCategory
