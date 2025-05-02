from fastapi import Request, HTTPException
from middleware.jwt import verify_token


async def route_middleware(request: Request):
    try:
        bearer_token = request.headers.get("authorization")
        [_, token] = bearer_token.split(" ")
        data = verify_token(token)

        if data is None:
            raise HTTPException(status_code=401, detail="invalid_credentials")

        request.user_data = data
    except Exception:
        raise HTTPException(status_code=401, detail="invalid_credentials")
