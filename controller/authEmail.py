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
from services.users import find_user, create_new_user
from fastapi import HTTPException


def authEmailController(email):
    redis_client.setex(f"email:auth-code:{email}", 330, generateCode())
    # todo send_email

    return {"message": "code_sended"}


async def authEmailCodeController(email, code, db):
    stored_code = redis_client.get(f"email:auth-code:{email}")

    if not stored_code or stored_code != code:
        raise HTTPException(status_code=400, detail=str("Código inválido"))

    redis_client.delete(f"email:auth-code:{email}")

    userData = await find_user(email, db)

    if userData is None:
        success = await create_new_user(email, db)
        if success:
            userData = await find_user(email, db)
        else:
            raise HTTPException(status_code=500, detail=str("Erro ao criar usuário"))

    token = createAccessToken(userData)

    return {"token": token}
