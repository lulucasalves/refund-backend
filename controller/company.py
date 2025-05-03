from services.company import get_company_service, update_company_service
from fastapi import HTTPException


async def get_company_controller(body, req, db):
    filters = body.filters
    userId = req.user_data["user_id"]

    return await get_company_service(filters, userId, db)


async def update_company_controller(body, req, db):
    create = body.create
    edit = body.edit
    delete = body.delete
    ambientId = body.ambientId

    user_ambients = req.user_data.get("ambients", [])
    if ambientId not in [amb["ambient_id"] for amb in user_ambients]:
        raise HTTPException(status_code=403, detail="ambient_no_permission")

    userId = req.user_data["user_id"]

    return await update_company_service(create, edit, delete, ambientId, userId, db)
