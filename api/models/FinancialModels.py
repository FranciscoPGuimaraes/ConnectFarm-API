from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class FinancialCategory(str, Enum):
    FEEDING = "feeding"
    PRODUCTION = "production"


class FinancialTransactionIn(BaseModel):
    transaction_type: str  # "exit" or "entry"
    description: str
    value: float
    date: datetime
    matriz_id: Optional[List[int]] = None
    category: FinancialCategory


class FinancialTransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    date: Optional[datetime] = None
    matriz_id: Optional[List[int]] = None
    category: Optional[FinancialCategory] = None


class FinancialTransaction(BaseModel):
    id: str = Field(alias="_id")
    transaction_type: str
    description: str
    value: float
    date: datetime
    matriz_id: Optional[List[int]] = None
    category: FinancialCategory
