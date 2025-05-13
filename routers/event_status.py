from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.event_status import get_event_status_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/event-status", tags=["event-status"])


class GetEventStatusBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_event_status(
    body: GetEventStatusBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_event_status_controller, body, request, db)
