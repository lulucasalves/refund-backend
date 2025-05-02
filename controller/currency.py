from services.currency import get_currency_service


async def get_currency_controller(body, req, db):
    filters = body.filters

    return await get_currency_service(filters, db)
