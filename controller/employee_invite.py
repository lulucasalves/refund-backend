from services.employee_invite import (
    verify_employee_invite_service,
    get_employee_invite_service,
)


async def get_employee_invite_controller(_, req, db):
    user_id = req.user_data["user_id"]

    return await get_employee_invite_service(user_id, db)


async def verify_employee_invite_controller(body, req, db):
    status = body["status"]
    employee_id = body["employee_id"]
    user_id = req.user_data["user_id"]

    return await verify_employee_invite_service(employee_id, status, user_id, db)
