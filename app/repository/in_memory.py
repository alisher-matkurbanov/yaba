import uuid
from functools import wraps
from pprint import pprint

from app.core.entity import ChatMessage, SavedChatMessage, UpdateChatMessage
from app.repository.interface import ChatRepositoryInterface, UserID, SessionID, ChatHistory


class DatabaseError(Exception):
    pass


def transform_exception(exc_type):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise exc_type() from e

        return wrapper

    return decorator


def log_database(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"before {func.__name__}")
        pprint(args[0].database)
        res = await func(*args, **kwargs)
        print(f"after {func.__name__}")
        pprint(args[0].database)
        return res

    return wrapper


class ChatInMemoryRepository(ChatRepositoryInterface):
    database: dict[UserID, dict[SessionID, ChatHistory]] = dict()

    def __init__(self):
        # todo: add concurrency control!
        pass

    @transform_exception(DatabaseError)
    async def get_chat_message(self, chat_message: ChatMessage) -> SavedChatMessage | None:
        user_sessions = self.database.get(chat_message.user_id)
        if user_sessions is None:
            return None

        session_messages = user_sessions.get(chat_message.session_id)
        if session_messages is None:
            return None

        for message in session_messages:
            if message.idempotency_key == chat_message.idempotency_key:
                return message

        return

    @transform_exception(DatabaseError)
    async def save_chat_message(self, chat_message: ChatMessage) -> SavedChatMessage:
        saved_message = SavedChatMessage(
            message_id=str(uuid.uuid4()),  # generate id on message save
            user_id=chat_message.user_id,
            session_id=chat_message.session_id,
            idempotency_key=chat_message.idempotency_key,
            input=chat_message.input,
        )
        if chat_message.user_id not in self.database:
            self.database[chat_message.user_id] = dict()

        if chat_message.session_id not in self.database[chat_message.user_id]:
            self.database[chat_message.user_id][chat_message.session_id] = list()

        self.database[chat_message.user_id][chat_message.session_id].append(saved_message)
        return saved_message

    @transform_exception(DatabaseError)
    async def update_chat_message(self, update_message: UpdateChatMessage) -> SavedChatMessage:
        sessions = self.database.get(update_message.user_id)
        if sessions is None:
            raise DatabaseError(f"user '{update_message.user_id}' not found")

        messages = sessions.get(update_message.session_id)
        if messages is None:
            raise DatabaseError(f"session '{update_message.session_id}' not found of user '{update_message.user_id}'")

        for index, message in enumerate(messages):
            if message.message_id == update_message.message_id:
                self.database[update_message.user_id][update_message.session_id][index].output = update_message.output
                return

        raise DatabaseError(f"message '{update_message.message_id}' not found in session '{update_message.session_id}' "
                            f"of user '{update_message.user_id}'")

    @transform_exception(DatabaseError)
    async def get_history(self, user_id: str, session_id: str) -> ChatHistory:
        sessions = self.database.get(user_id)
        if sessions is None:
            return []

        messages = sessions.get(session_id)
        if messages is None:
            return []

        return messages
