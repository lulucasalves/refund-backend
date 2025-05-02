from services.auth import generate_email_code_service, auth_email_service
from database.mysql import get_db


async def generate_email_code_controller(body, req):
    email = body.email

    return await generate_email_code_service(email)


get_db()


async def auth_email_controller(body, req, db):
    email = body.email
    code = body.code
    client_host = req.client.host

    return await auth_email_service(email, code, client_host, db)
