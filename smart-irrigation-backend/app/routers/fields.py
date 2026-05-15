from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..schemas import FieldCreate, FieldRead
from ..crud import create_field, get_fields, get_field

router = APIRouter(prefix="/fields", tags=["fields"])

@router.post("/", response_model=FieldRead)
def create_field_endpoint(field: FieldCreate, session: Session = Depends(get_session)):
    f = create_field(session, field.dict())
    return f

@router.get("/", response_model=List[FieldRead])
def list_fields(session: Session = Depends(get_session)):
    return get_fields(session)

@router.get("/{field_id}", response_model=FieldRead)
def get_field_endpoint(field_id: int, session: Session = Depends(get_session)):
    f = get_field(session, field_id)
    if not f:
        raise HTTPException(status_code=404, detail="Field not found")
    return f
@router.get("/{field_id}", response_model=FieldRead)
def get_field_endpoint(field_id: int, session: Session = Depends(get_session)):
    f = get_field(session, field_id)
    if not f:
        raise HTTPException(status_code=404, detail="Field not found")
    return f