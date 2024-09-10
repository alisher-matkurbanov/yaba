from fastapi import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


async def check_idempotency_key(request: Request, call_next):
    if request.headers.get("Idempotency-Key") is None:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": "Idempotency-Key header is required"},
        )

    return await call_next(request)
