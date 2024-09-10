from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.handler import chat, middleware

app = FastAPI()
app.include_router(chat.router)
app.add_middleware(BaseHTTPMiddleware, dispatch=middleware.check_idempotency_key)
