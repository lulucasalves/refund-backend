from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.company_status import get_company_status_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/company-status", tags=["company-status"])


class GetCompanyStatusBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_company_status(
    body: GetCompanyStatusBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_company_status_controller, body, request, db)
