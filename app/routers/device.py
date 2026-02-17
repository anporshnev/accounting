from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.schemas.device import DeviceFromDB, DeviceCreate
from app.models.device import Device
from app.database import get_session

device_router: APIRouter = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

@device_router.get("/", response_model=list[DeviceFromDB])
async def get_devices(sesssion: AsyncSession = Depends(get_session)):
    result = await sesssion.execute(select(Device))
    return result.scalars().all()

@device_router.get("/{device_id}", response_model=DeviceFromDB)
async def get_device_by_id(device_id: UUID, sesssion: AsyncSession = Depends(get_session)):
    device = await sesssion.get(Device, device_id)
    return device

@device_router.post("/")
async def add_device(group: DeviceCreate, sesssion: AsyncSession = Depends(get_session)):
    new_group = Device(**group.model_dump())
    sesssion.add(new_group)
    try:
        await sesssion.commit()
    except SQLAlchemyError:
        await sesssion.rollback()
        raise
    
@device_router.put("/{device_id}")
async def update_device(device_id: UUID, group: DeviceCreate, sesssion: AsyncSession = Depends(get_session)):
    new_data = group.model_dump()
    try:
        record = await sesssion.get(Device, device_id)
        if record:
            for key, value in new_data.items():
                setattr(record, key, value)
                
            
            await sesssion.commit()
    except SQLAlchemyError:
        await sesssion.rollback()
        raise
    
@device_router.delete("/{device_id}")
async def delete_group(device_id: UUID, sesssion: AsyncSession = Depends(get_session)):
    device = await sesssion.get(Device, device_id)
    if device:
        await sesssion.delete(device)
        await sesssion.commit()