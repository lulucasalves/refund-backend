from fastapi import HTTPException
from utils.country_ip import get_country_from_ip
from database.redis import redis_client
from middleware.jwt import create_access_token
from services.user import find_user_auth_info, create_user
from utils.code_generator import generate_code


async def generate_email_code_service(email):
    redis_client.setex(f"email:auth-code:{email}", 330, generate_code())

    return {"message": "code_sended"}


async def auth_email_service(email, code, client_host, db):
    try:
        stored_code = redis_client.get(f"email:auth-code:{email}")

        country = get_country_from_ip(client_host)

        if not stored_code or stored_code != code:
            raise HTTPException(status_code=400, detail="invalid_code")

        redis_client.delete(f"email:auth-code:{email}")

        userData = await find_user_auth_info(email, db)

        if userData is None:
            success = await create_user(email, country, db)
            if success:
                userData = await find_user_auth_info(email, db)
            else:
                raise HTTPException(status_code=500, detail="create_user_error")

        token = create_access_token(userData)

        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
