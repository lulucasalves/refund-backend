from fastapi import HTTPException
from translator import t


async def controller(function, body, req, db=None):
    try:
        if db is None:
            return await function(body, req)
        else:
            return await function(body, req, db)
    except Exception as e:
        accept_language = req.headers.get("Accept-Language") or "en"

        print(e.detail)
        if hasattr(e, "detail"):
            [status_code, detail] = e.detail.split(": ")

            raise HTTPException(
                status_code=int(status_code), detail=t(detail, accept_language)
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))
