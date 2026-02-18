from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.schemas.group import GroupFromDB, GroupCreate
from app.models.group import Group
from app.database import get_session
from app.errors import AddingException, UpdateException

group_router: APIRouter = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

@group_router.get("/", response_model=list[GroupFromDB])
async def get_groups(sesssion: AsyncSession = Depends(get_session)):
    result = await sesssion.execute(select(Group))
    return result.scalars().all()

@group_router.post("/", response_model=GroupFromDB)
async def add_group(group: GroupCreate, sesssion: AsyncSession = Depends(get_session)):
    group_dict = group.model_dump()
    new_group = Group(**group_dict)
    sesssion.add(new_group)
    try:
        await sesssion.flush()
        response = GroupFromDB(id=new_group.id,**group_dict)
        await sesssion.commit()
    except SQLAlchemyError as e:
        await sesssion.rollback()
        raise AddingException(e)
    return response
    
@group_router.put("/{group_id}")
async def update_group(group_id: int, group: GroupCreate, sesssion: AsyncSession = Depends(get_session)):
    record = await sesssion.get(Group, group_id)
    if record:
        record.title = group.title   
    try:
        await sesssion.commit()
    except SQLAlchemyError as e:
        await sesssion.rollback()
        raise UpdateException(e)
    return group
    
@group_router.delete("/{group_id}")
async def delete_group(group_id: int, sesssion: AsyncSession = Depends(get_session)):
    room = await sesssion.get(Group, group_id)
    if room:
        await sesssion.delete(room)
        await sesssion.commit()