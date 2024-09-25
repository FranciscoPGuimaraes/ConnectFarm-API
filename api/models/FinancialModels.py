from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class FinancialCategory(str, Enum):
    ALIMENTAÇÃO = "Alimentação"
    SAÚDE_ANIMAL = "Saúde animal"
    VACINAÇÃO = "Vacinação"
    REPRODUÇÃO = "Reprodução"
    MANUTENÇÃO_PASTAGENS = "Manutenção das pastagens"
    CUSTOS_MÃO_DE_OBRA = "Custos de mão-de-obra"
    TRANSPORTE_GADO = "Transporte do gado"
    SUPLEMENTAÇÃO = "Suplementação"
    LUCRO_PRODUCAO = ("Lucro com produção",)
    LUCRO_VENDA_GADO = "Lucro com venda de gado"


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
