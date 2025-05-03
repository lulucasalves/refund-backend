from services.date_format import get_date_format_service


async def get_date_format_controller(body, req, db):
    filters = body.filters

    return await get_date_format_service(filters, db)
