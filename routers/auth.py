from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sys
from sqlalchemy.orm import Session
from services.users import get_db

sys.path.append("..")
from controller.authEmail import authEmailController, authEmailCodeController

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthEmailRequest(BaseModel):
    email: str


class AuthEmailCodeRequest(BaseModel):
    email: str
    code: str


@router.post("/email")
async def authEmail(
    request: AuthEmailRequest,
):
    return authEmailController(request.email)


@router.post("/email-code")
async def authEmailCode(request: AuthEmailCodeRequest, db: Session = Depends(get_db)):
    return await authEmailCodeController(request.email, request.code, db)
