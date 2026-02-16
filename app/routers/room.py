from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.schemas.room import RoomFromDB, RoomCreate
from app.models.room import Room
from app.database import get_session

room_router: APIRouter = APIRouter(
    prefix="/rooms",
    tags=["Room"]
)

@room_router.get("/", response_model=list[RoomFromDB])
async def get_rooms(sesssion: AsyncSession = Depends(get_session)):
    result = await sesssion.execute(select(Room))
    return result.scalars().all()

@room_router.post("/")
async def add_room(room: RoomCreate, sesssion: AsyncSession = Depends(get_session)):
    new_room = Room(**room.model_dump())
    sesssion.add(new_room)
    try:
        await sesssion.commit()
    except SQLAlchemyError:
        await sesssion.rollback()
        raise 
    
@room_router.put("/{room_id}")
async def update_room(room_id: int, room: RoomCreate, sesssion: AsyncSession = Depends(get_session)):
    record = await sesssion.get(Room, room_id)
    try:
        if record:
            record.title = room.title
            await sesssion.commit()
        return None
    except SQLAlchemyError:
        await sesssion.rollback()
        raise
    

@room_router.delete("/{room_id}")
async def delete_room(room_id: int, sesssion: AsyncSession = Depends(get_session)):
    room = await sesssion.get(Room, room_id)
    if room:
        await sesssion.delete(room)
        await sesssion.commit()