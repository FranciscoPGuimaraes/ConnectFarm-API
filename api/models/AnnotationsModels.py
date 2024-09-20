from uuid import UUID
from pydantic import BaseModel, Field


class Annotations(BaseModel):
    date: str = Field(max_length=50)
    description: str = Field(max_length=30)
