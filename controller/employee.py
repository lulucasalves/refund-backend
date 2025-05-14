from services.employee import (
    get_employee_service,
    update_employee_service,
    verify_employee_service,
)


async def get_employee_controller(body, req, db):
    filters = body.filters
    user_id = req.user_data["user_id"]

    return await get_employee_service(filters, user_id, db)


async def verify_employee_controller(code, _, db):
    return await verify_employee_service(code, db)


async def update_employee_controller(body, _, db):
    create = body.create
    edit = body.edit
    delete = body.delete
    company_id = body.companyId

    return await update_employee_service(create, edit, delete, company_id, db)
