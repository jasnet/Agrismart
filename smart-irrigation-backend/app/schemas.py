from pydantic import BaseModel
from typing import Optional
from datetime import date

class FieldCreate(BaseModel):
    name: str
    area_m2: float
    soil_type: str
    crop_type: str
    crop_stage: str
    irrigation_method: str
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None

class FieldRead(FieldCreate):
    id: int

class SensorRead(BaseModel):
    id: int
    name: str
    type: str
    last_value: Optional[float]

class SensorCreate(BaseModel):
    name: str
    type: str
    field_id: int

class ScheduleEntry(BaseModel):
    date: date
    water_mm: float
    volume_liters: float
    duration_min: float
    status: str