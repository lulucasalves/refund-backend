from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.date_format import get_date_format_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/date-format", tags=["date-format"])


class GetDateFormatBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_date_format(
    body: GetDateFormatBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_date_format_controller, body, request, db)
