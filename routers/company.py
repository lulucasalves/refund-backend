from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.company import get_company_controller, update_company_controller
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/company", tags=["company"])


class GetCompanyBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_company(
    body: GetCompanyBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_company_controller, body, request, db)


class UpdateCompanyBody(BaseModel):
    create: list = []
    edit: list = []
    delete: list = []
    ambientId: str


@router.post("/update")
async def update_company(
    body: UpdateCompanyBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(update_company_controller, body, request, db)
