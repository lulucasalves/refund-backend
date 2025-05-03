from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.ambient import update_ambient_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/ambient", tags=["ambient"])


class GetAmbientBody(BaseModel):
    name: str
    ambientId: str


@router.post("/update")
async def update_ambient(
    body: GetAmbientBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(update_ambient_controller, body, request, db)
