from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.event import get_event_controller, update_event_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/event", tags=["event"])


class GetEventBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_event(
    body: GetEventBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_event_controller, body, request, db)


class UpdateEventBody(BaseModel):
    create: list = []
    edit: list = []
    delete: list = []
    companyId: str

@router.post("/update")
async def update_event(
    body: UpdateEventBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(update_event_controller, body, request, db)
