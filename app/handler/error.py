import logging
from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.exceptions import ValidationException

from fastapi.routing import APIRoute
from starlette import status

logger = logging.getLogger("chat")


class ErrorHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except ValidationException as e:
                logger.exception(e)
                raise
            except Exception as e:
                print(type(e))
                logger.exception(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")

        return custom_route_handler
