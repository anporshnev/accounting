from pydantic import BaseModel, UUID4
from datetime import datetime

class DeviceFromDB(BaseModel):
    id: UUID4
    title: str
    model: str | None
    inventory_number: str | None
    serial_number: str | None
    room_id: int
    group_id: int
    properties: dict | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    
class DeviceCreate(BaseModel):
    title: str
    model: str | None
    inventory_number: str | None
    serial_number: str | None
    room_id: int
    group_id: int
    properties: dict | None
    notes: str | None