from dataclasses import dataclass


@dataclass
class ChatMessage:
    user_id: str
    session_id: str
    input: str
    idempotency_key: str


@dataclass
class UpdateChatMessage:
    message_id: str
    user_id: str
    session_id: str
    output: str


@dataclass
class SavedChatMessage:
    message_id: str
    user_id: str
    session_id: str
    idempotency_key: str
    input: str
    output: str | None = None


@dataclass
class ChatAnswer:
    output: str
