from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
from services.users import find_user, get_db

sys.path.append("..")
from services.users import find_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_user(db: Session = Depends(get_db)):
    user = await find_user("dsfd@wjod.com", db)
    return {"success": user}
