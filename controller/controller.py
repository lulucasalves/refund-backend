from fastapi import HTTPException
from translator import t
import asyncio


async def controller(function, body, req, db=None):
    try:
        # await asyncio.sleep(2)
        if db is None:
            return await function(body, req)
        else:
            return await function(body, req, db)
    except Exception as e:
        accept_language = req.headers.get("Accept-Language") or "en"

        if hasattr(e, "status_code") and hasattr(e, "detail"):
            raise HTTPException(
                status_code=int(e.status_code), detail=t(e.detail, accept_language)
            )
        elif hasattr(e, "detail"):
            print(e)
            [status_code, detail] = e.detail.split(": ")

            raise HTTPException(
                status_code=int(status_code), detail=t(detail, accept_language)
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))
