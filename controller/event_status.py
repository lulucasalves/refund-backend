from services.event_status import get_event_status_service


async def get_event_status_controller(body, req, db):
    filters = body.filters

    return await get_event_status_service(filters,db)
