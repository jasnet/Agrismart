from sqlmodel import select
from .models import Field, Sensor, Schedule
from .database import get_session, engine
from typing import List
from datetime import datetime

# Small CRUD helpers used by routers

def create_field(session, field_data) -> Field:
    f = Field(**field_data)
    session.add(f)
    session.commit()
    session.refresh(f)
    return f

def get_fields(session) -> List[Field]:
    return session.exec(select(Field)).all()

def get_field(session, field_id: int) -> Field | None:
    return session.get(Field, field_id)

def create_sensor(session, sensor_data) -> Sensor:
    s = Sensor(**sensor_data)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s

def update_sensor_value(session, sensor_id: int, value: float):
    s = session.get(Sensor, sensor_id)
    if not s:
        return None
    s.last_value = value
    s.last_updated = datetime.utcnow()
    session.add(s)
    session.commit()
    session.refresh(s)
    return s

def save_schedule_entries(session, entries):
    for e in entries:
        s = Schedule(**e)
        session.add(s)
    session.commit()