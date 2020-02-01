from fastapi import APIRouter

router = APIRouter()


@router.get("/basement/")
async def get_basement_data():
    return {"message": "Hello World"}


@router.get("/strong-floor/")
async def get_strong_floor_data():
    return {"message": "Hello World"}


@router.get("/steel-frame/")
async def get_steel_frame_data():
    return {"message": "Hello World"}
