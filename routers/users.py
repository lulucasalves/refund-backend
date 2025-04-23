from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_user():
    return {"success": True}
