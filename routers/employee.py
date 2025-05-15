from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.employee import (
    get_employee_controller,
    update_employee_controller,
)
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/employee", tags=["employee"])


class GetEmployeeBody(BaseModel):
    filters: dict = {}


@router.post("/")
async def get_employee(
    body: GetEmployeeBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_employee_controller, body, request, db)


class UpdateEmployeeBody(BaseModel):
    create: list = []
    edit: list = []
    delete: list = []
    companyId: str


@router.post("/update")
async def update_employee(
    body: UpdateEmployeeBody,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(update_employee_controller, body, request, db)
