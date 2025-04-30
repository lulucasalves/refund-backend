import sys

sys.path.append("..")
from utils.codeGenerator import generateCode
import sys

sys.path.append("..")
from database.redis import redis_client

import sys

sys.path.append("..")
from middleware.jwt import createAccessToken


import sys

sys.path.append("..")
from services.users import find_user


def authEmailController(email):
    redis_client.setex(f"email:auth-code:{email}", 300, generateCode())
    # todo send_email

    return {"message": "code_sended"}


async def authEmailCodeController(email, code):
    stored_code = redis_client.get(f"email:auth-code:{email}")

    if not stored_code or stored_code != code:
        return {"error": "Código inválido"}, 400

    redis_client.delete(f"email:auth-code:{email}")

    userData = await find_user(email)
    token = createAccessToken(userData)
    
    return {"token": token, "userData": userData}
