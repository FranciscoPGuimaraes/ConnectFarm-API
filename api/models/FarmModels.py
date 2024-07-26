from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FarmOut(BaseModel):
    farm_id: UUID
    name: str = Field(max_length=60)
    address: str = Field(max_length=150)


class FarmIn(BaseModel):
    name: str = Field(max_length=60)
    address: str = Field(max_length=150)
    area: Optional[float]
    objective: Optional[str] = Field(None, max_length=30)
