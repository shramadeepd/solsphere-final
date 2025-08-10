from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.machine import CheckInPayload, MachineOut
from services.machine_service import upsert_machine_and_checks, list_machines, get_machine
from typing import List, Optional

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/report", status_code=status.HTTP_201_CREATED, response_model=MachineOut)
def report(payload: CheckInPayload, db: Session = Depends(get_db)):
    machine = upsert_machine_and_checks(db, payload)
    return machine


@router.get("/machines", response_model=List[MachineOut])
def api_list_machines(os: Optional[str] = None, status: Optional[str] = None, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    machines = list_machines(db=db, os_name=os, status=status, limit=limit, offset=offset)
    return machines


@router.get("/machines/{id}", response_model=MachineOut)
def api_get_machine(id: int, db: Session = Depends(get_db)):
    m = get_machine(db, id)
    if not m:
        raise HTTPException(status_code=404, detail="Machine not found")
    return m
