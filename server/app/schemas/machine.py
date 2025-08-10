from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CheckInCheck(BaseModel):
    name: str
    status: str
    details: Optional[Dict[str, Any]] = None


class CheckInPayload(BaseModel):
    machine_id: str
    hostname: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    checks: Optional[List[CheckInCheck]] = []


class CheckResultOut(BaseModel):
    id: int
    check_name: str
    status: str
    details: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class MachineOut(BaseModel):
    id: int
    machine_id: str
    hostname: Optional[str]
    os_name: Optional[str]
    os_version: Optional[str]
    last_checkin: datetime
    metadata: Optional[Dict[str, Any]] = Field(alias="machine_metadata")
    checks: List[CheckResultOut] = []

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }