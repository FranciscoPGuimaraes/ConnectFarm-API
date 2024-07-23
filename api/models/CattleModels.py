from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import date


class Age(BaseModel):
    value: int
    date: date


class Weight(BaseModel):
    date: date
    weight: float
    observation: Optional[str]


class Location(BaseModel):
    date: date
    latitude: float
    longitude: float


class Vaccine(BaseModel):
    date: date
    type: str


class HealthHistory(BaseModel):
    date: date
    status: str
    disease: Optional[str]
    
    
class Calf(BaseModel):
    calf_id: str
    birth_date: date
    weaning: date
    annotation: Optional[str]
    weights: List[Weight]
    vaccines: List[Vaccine]
    health_history: List[HealthHistory]


class Reproduction(BaseModel):
    type: str
    date: date


class Cattle(BaseModel):
    id: str = Field(alias="_id")
    farm_id: UUID
    number: int
    age: Optional[Age]
    breed: str
    annotation: Optional[str]
    weights: List[Weight]
    locations: List[Location]
    calves: List[Calf]
    vaccines: List[Vaccine]
    reproduction: List[Reproduction]
    health_history: List[HealthHistory]
