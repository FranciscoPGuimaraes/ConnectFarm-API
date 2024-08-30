from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class Age(BaseModel):
    value: int
    date: str

class Weight(BaseModel):
    date: str
    weight: float
    observation: Optional[str] = None

class Location(BaseModel):
    date: str
    latitude: float
    longitude: float

class VaccineIn(BaseModel):
    date: str
    type: str

class Vaccine(BaseModel):
    id: str
    date: str
    type: str

class VaccineUpdate(BaseModel):
    date: Optional[str]
    type: Optional[str]

class HealthHistory(BaseModel):
    date: str
    status: str
    disease: Optional[str] = None

class CalfIn(BaseModel):
    number: str
    birth_date: str
    weaning: Optional[str]
    annotation: Optional[str]
    weights: Weight

class CalfUpdate(BaseModel):
    number: Optional[str] = None
    birth_date: Optional[str] = None
    weaning: Optional[str] = None
    annotation: Optional[str] = None
    weights: Optional[Weight] = None
    health_history: Optional[HealthHistory] = None

class Calf(BaseModel):
    number: str
    birth_date: str
    weaning: Optional[str]
    annotation: Optional[str]
    weights: List[Weight] = []
    vaccines: List[Vaccine] = []
    health_history: List[HealthHistory] = []

class Reproduction(BaseModel):
    type: str
    date: str

class CattleIn(BaseModel):
    farm_id: Optional[UUID] = None
    number: int
    age: Optional[Age] = None
    breed: str
    annotation: Optional[str] = None
    weights: Weight

class CattleUpdate(BaseModel):
    number: Optional[int] = None
    weights: Optional[Weight] = None
    reproduction: Optional[Reproduction] = None
    health_history: Optional[HealthHistory] = None

class Cattle(BaseModel):
    id: str = Field(alias="_id")
    farm_id: UUID
    number: int
    age: Optional[Age] = None  # Ensure this field is optional
    breed: str
    annotation: Optional[str] = None
    weights: List[Weight] = []
    locations: List[Location] = []
    calves: List[Calf] = []
    vaccines: List[Vaccine] = []
    reproduction: List[Reproduction] = []
    health_history: List[HealthHistory] = []
