from pydantic import BaseModel

class GroupFromDB(BaseModel):
    id: int
    title: str
    

class GroupCreate(BaseModel):
    title: str