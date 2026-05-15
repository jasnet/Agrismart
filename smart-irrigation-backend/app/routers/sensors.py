from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..schemas import SensorCreate, SensorRead
from ..crud import create_sensor, update_sensor_value
from ..models import Sensor

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.post("/", response_model=SensorRead)
def create_sensor_endpoint(sensor: SensorCreate, session: Session = Depends(get_session)):
    return create_sensor(session, sensor.dict())

@router.put("/{sensor_id}/value", response_model=SensorRead)
def update_value(sensor_id: int, value: float, session: Session = Depends(get_session)):
    s = update_sensor_value(session, sensor_id, value)
    if not s:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return s
