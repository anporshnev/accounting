from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.schemas.device import DeviceFromDB, DeviceCreate
from app.models.device import Device
from app.database import get_session
from app.errors import AddingException, UpdateException
from app.utils import get_hash

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
async def add_device(device: DeviceCreate, sesssion: AsyncSession = Depends(get_session)):
    new_device_hash = get_hash(
        device.title, 
        device.model, 
        device.inventory_number, 
        device.serial_number
        )
    
    query = select(Device).filter(Device.hash == new_device_hash)
    devices = await sesssion.execute(query)
    if devices.first() is not None:
        raise HTTPException(
            status_code=400, 
            detail="Такое устройство уже существует")
    
    device_dict = device.model_dump()
    new_device = Device(hash=new_device_hash, **device_dict)
    sesssion.add(new_device)
    try:
        await sesssion.flush()
        response = DeviceFromDB(
            id=new_device.id,
            created_at=new_device.created_at,
            updated_at=new_device.updated_at,
            **device_dict
        )
        await sesssion.commit() 
    except SQLAlchemyError as e:
        await sesssion.rollback()
        raise AddingException(e)
    return response
 
@device_router.put("/{device_id}", response_model=DeviceCreate)
async def update_device(device_id: UUID, group: DeviceCreate, sesssion: AsyncSession = Depends(get_session)):
    new_data = group.model_dump()
    record = await sesssion.get(Device, device_id)
    if record:
        for key, value in new_data.items():
                setattr(record, key, value)
    try:
        await sesssion.commit()    
    except SQLAlchemyError as e:
        await sesssion.rollback()
        raise UpdateException(e)
    return new_data
    
@device_router.delete("/{device_id}")
async def delete_group(device_id: UUID, sesssion: AsyncSession = Depends(get_session)):
    device = await sesssion.get(Device, device_id)
    if device:
        await sesssion.delete(device)
        await sesssion.commit()