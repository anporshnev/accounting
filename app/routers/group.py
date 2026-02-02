from fastapi import APIRouter


room_router: APIRouter = APIRouter(
    prefix="/room",
    tags=["Room"]
)

@room_router.get("/")
async def get_room():
    pass

@room_router.post("/")
async def add_room():
    pass