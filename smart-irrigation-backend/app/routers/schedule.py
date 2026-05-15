from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..crud import get_field, save_schedule_entries
from ..scheduler import schedule_for_field
from ..schemas import ScheduleEntry

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.post("/calculate/{field_id}", response_model=List[ScheduleEntry])
async def calculate_schedule(field_id: int, days: int = 7, session: Session = Depends(get_session)):
    field = get_field(session, field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    
    # Convert SQLModel to dict for the scheduler helper
    field_dict = field.dict()
    
    # You might want to get recent sensor data to add "soil_moisture_pct" to field_dict
    # For now we skip that or assume it's not present (defaulting to dry logic)
    
    schedule = await schedule_for_field(field_dict, days=days, lat=field.location_lat, lon=field.location_lon)
    
    # Save to DB if desired, or just return
    # save_schedule_entries(session, schedule) 
    
    return schedule
