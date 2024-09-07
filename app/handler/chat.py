from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.handler.error import ErrorHandler
from app.service.chat import ChatService
from app.core.entity import ChatMessage
from app.schema import ChatMessageRequest, ChatAnswerResponse

router = APIRouter(route_class=ErrorHandler)


@router.post("/chat")
async def handle_chat_message(
        request: ChatMessageRequest,
        idempotency_key: Annotated[str, Header()],
        chat_service: ChatService = Depends(),
):
    message = ChatMessage(
        user_id=request.user_id,
        session_id=request.session_id,
        input=request.input,
        idempotency_key=idempotency_key,
    )
    answer = await chat_service.request_answer(message)
    return ChatAnswerResponse(output=answer.output)
