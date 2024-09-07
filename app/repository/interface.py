import abc
from typing import Union, TypeAlias

from app.core.entity import ChatMessage, SavedChatMessage, UpdateChatMessage

ChatHistory: TypeAlias = list[SavedChatMessage]
UserID: TypeAlias = str
SessionID: TypeAlias = str


class ChatRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    async def get_chat_message(self, chat_message: ChatMessage) -> Union[SavedChatMessage | None]:
        ...

    @abc.abstractmethod
    async def save_chat_message(self, chat_request: ChatMessage) -> SavedChatMessage:
        ...

    @abc.abstractmethod
    async def update_chat_message(self, message_id: UpdateChatMessage):
        ...

    @abc.abstractmethod
    async def get_history(self, user_id: UserID, session_id) -> ChatHistory:
        ...
