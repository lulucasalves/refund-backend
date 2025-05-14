from services.event import get_event_service, update_event_service


async def get_event_controller(body, req, db):
    filters = body.filters
    user_id = req.user_data["user_id"]

    return await get_event_service(filters, user_id, db)


async def update_event_controller(body, _, db):
    create = body.create
    edit = body.edit
    delete = body.delete
    company_id = body.companyId

    return await update_event_service(create, edit, delete, company_id, db)
