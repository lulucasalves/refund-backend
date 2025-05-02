from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.currency import get_currency_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/currency", tags=["currency"])


class GetCurrencyBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_currency(
    body: GetCurrencyBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_currency_controller, body, request, db)
