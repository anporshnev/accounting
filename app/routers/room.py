from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.room import RoomFromDB, RoomCreate
from app.models.room import Room
from app.database import get_session

room_router: APIRouter = APIRouter(
    prefix="/rooms",
    tags=["Room"]
)

@room_router.get("/", response_model=list[RoomFromDB])
async def get_room(sesssion: AsyncSession = Depends(get_session)):
    result = await sesssion.execute(select(Room))
    return result.scalars().all()

@room_router.post("/")
async def add_room(room: RoomCreate, sesssion: AsyncSession = Depends(get_session)):
    new_room = Room(**room.model_dump())
    sesssion.add(new_room)
    await sesssion.commit()

@room_router.delete("/{room_id}")
async def delete_room(sesssion: AsyncSession = Depends(get_session)):
    pass