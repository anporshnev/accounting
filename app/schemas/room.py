from pydantic import BaseModel

class RoomFromDB(BaseModel):
    id: int
    title: str
    

class RoomCreate(BaseModel):
    title: str