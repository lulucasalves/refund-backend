from fastapi import APIRouter
from pydantic import BaseModel
import sys

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
async def authEmailCode(
    request: AuthEmailCodeRequest,
):
    return authEmailCodeController(request.email, request.code)
