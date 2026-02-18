from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.schemas.room import RoomFromDB, RoomCreate
from app.schemas.device import DeviceFromDB
from app.models.room import Room
from app.models.device import Device
from app.database import get_session
from app.errors import AddingException, UpdateException

room_router: APIRouter = APIRouter(
    prefix="/rooms",
    tags=["Room"]
)

@room_router.get("/", response_model=list[RoomFromDB])
async def get_rooms(sesssion: AsyncSession = Depends(get_session)):
    result = await sesssion.execute(select(Room))
    return result.scalars().all()

@room_router.get("/{room_id}/devices", response_model=list[DeviceFromDB])
async def get_room_devices(room_id: int, sesssion: AsyncSession = Depends(get_session)):
    query = select(Device).filter(Device.room_id == room_id)
    result = await sesssion.execute(query)
    devices = result.scalars().all()
    return devices

@room_router.post("/")
async def add_room(room: RoomCreate, sesssion: AsyncSession = Depends(get_session)):
    new_room = Room(**room.model_dump())
    sesssion.add(new_room)
    try:
        await sesssion.commit()
    except SQLAlchemyError as e:
        await sesssion.rollback()
        raise AddingException(e)
    
@room_router.put("/{room_id}")
async def update_room(room_id: int, room: RoomCreate, sesssion: AsyncSession = Depends(get_session)):
    record = await sesssion.get(Room, room_id)
    try:
        if record:
            record.title = room.title
            await sesssion.commit()
    except SQLAlchemyError as e:
        await sesssion.rollback()
        raise UpdateException(e)
    

@room_router.delete("/{room_id}")
async def delete_room(room_id: int, sesssion: AsyncSession = Depends(get_session)):
    room = await sesssion.get(Room, room_id)
    query = select(Device).filter(Device.room_id == room_id)
    devices = await sesssion.execute(query)
    if devices.first() is not None:
        raise HTTPException(
            status_code=400, 
            detail="Помещение в котором есть оборудование не может быть удалено")
    if room:
        await sesssion.delete(room)
        await sesssion.commit()