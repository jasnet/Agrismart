from typing import Optional, List
from sqlmodel import SQLModel, Field as DBField, Relationship
from datetime import datetime

class Sensor(SQLModel, table=True):
    id: Optional[int] = DBField(default=None, primary_key=True)
    name: str
    type: str # e.g. soil_moisture, flow
    last_value: Optional[float] = None
    last_updated: Optional[datetime] = None
    field_id: Optional[int] = DBField(default=None, foreign_key="field.id")
    
    field: Optional["Field"] = Relationship(back_populates="sensors")

class Field(SQLModel, table=True):
    id: Optional[int] = DBField(default=None, primary_key=True)
    name: str
    area_m2: float
    soil_type: str # sandy, loamy, clay
    crop_type: str
    crop_stage: str # sowing, vegetative, flowering, maturity
    irrigation_method: str # drip, sprinkler, flood
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    sensors: List[Sensor] = Relationship(back_populates="field")

class Schedule(SQLModel, table=True):
    id: Optional[int] = DBField(default=None, primary_key=True)
    field_id: int = DBField(foreign_key="field.id")
    date: datetime
    water_mm: float
    volume_liters: float
    duration_min: float
    status: str = "scheduled" # scheduled, executed, skipped, manual

class Log(SQLModel, table=True):
    id: Optional[int] = DBField(default=None, primary_key=True)
    field_id: Optional[int]
    action: str
    timestamp: datetime
    details: Optional[str] = None