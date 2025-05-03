from services.company_status import get_company_status_service


async def get_company_status_controller(body, req, db):
    filters = body.filters

    return await get_company_status_service(filters,db)
