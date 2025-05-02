from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.auth import generate_email_code_controller, auth_email_controller
from controller.controller import controller

router = APIRouter(prefix="/auth", tags=["auth"])


class GenerateEmailCodeBody(BaseModel):
    email: str


@router.post("/generate-email-code")
async def generate_email_code(
    body: GenerateEmailCodeBody,
    request: Request,
):
    return await controller(generate_email_code_controller, body, request)


class EmailBody(BaseModel):
    email: str
    code: str


@router.post("/email")
async def email(body: EmailBody, request: Request, db: Session = Depends(get_db)):
    return await controller(auth_email_controller, body, request, db)
