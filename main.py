import uvicorn
from fastapi import FastAPI
from app.routers.room import room_router
from app.routers.group import group_router
from app.routers.device import device_router

app = FastAPI()

app.include_router(room_router)
app.include_router(group_router)
app.include_router(device_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

