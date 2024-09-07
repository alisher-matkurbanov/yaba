from fastapi.params import Depends

from app.core.entity import ChatMessage, ChatAnswer, UpdateChatMessage
from app.client.llm_client import LLMClient
from app.repository.in_memory import ChatInMemoryRepository, ChatRepositoryInterface


class DatabaseError(Exception):
    pass


class LLMError(Exception):
    pass


class ChatService:
    chat_repo: ChatRepositoryInterface
    llm_client: LLMClient

    def __init__(
            self,
            chat_repo: ChatInMemoryRepository = Depends(),
            llm_client: LLMClient = Depends(),
    ):
        self.chat_repo = chat_repo
        self.llm_client = llm_client

    async def request_answer(self, message: ChatMessage) -> ChatAnswer:
        # check if there is same user's message
        saved_message = await self.chat_repo.get_chat_message(message)
        if saved_message is not None:
            return ChatAnswer(output=saved_message.output)

        history = await self.chat_repo.get_history(message.user_id, message.session_id)
        saved_message = await self.chat_repo.save_chat_message(message)
        answer = await self.llm_client.request_answer(message, history)
        update_message = UpdateChatMessage(
            message_id=saved_message.message_id,
            user_id=message.user_id,
            session_id=message.session_id,
            output=answer.output,
        )
        await self.chat_repo.update_chat_message(update_message)
        return answer
