from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from database.mysql import get_db
from sqlalchemy.orm import Session
from controller.employee_invite import (
    get_employee_invite_controller,
    verify_employee_invite_controller,
)
from controller.controller import controller
from middleware.route_middleware import route_middleware

router = APIRouter(prefix="/employee-invite", tags=["employee-invite"])


class GetEmployeeInviteBody(BaseModel):
    filters: dict = {}


@router.get("/")
async def get_employee_invite(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(get_employee_invite_controller, {}, request, db)


@router.get("/verify/{employee_id}/{status}")
async def verify_employee(
    status: str,
    employee_id: str,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(route_middleware),
):
    return await controller(
        verify_employee_invite_controller,
        {"status": status, "employee_id": employee_id},
        request,
        db,
    )
