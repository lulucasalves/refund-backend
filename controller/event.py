from services.event import get_event_service, update_event_service


async def get_event_controller(body, req, db):
    filters = body.filters
    userId = req.user_data["user_id"]

    return await get_event_service(filters, userId, db)


async def update_event_controller(body, req, db):
    create = body.create
    edit = body.edit
    delete = body.delete
    companyId = body.companyId

    return await update_event_service(create, edit, delete, companyId, db)
