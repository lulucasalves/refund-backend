from services.ambient import update_ambient_service
from fastapi import HTTPException


async def update_ambient_controller(body, req, db):
    ambientId = body.ambientId
    name = body.name

    user_ambients = req.user_data.get("ambients", [])
    if ambientId not in [amb["ambient_id"] for amb in user_ambients]:
        raise HTTPException(status_code=403, detail="ambient_no_permission")

    return await update_ambient_service(name, ambientId, db)
