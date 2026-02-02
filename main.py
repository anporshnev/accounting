import uvicorn
from fastapi import FastAPI
from app.routers.group import room_router

app = FastAPI()

app.include_router(room_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

