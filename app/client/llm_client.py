from app.core.entity import ChatMessage, ChatAnswer
from app.repository.in_memory import ChatHistory


class LLMClient:
    def __init__(self):
        # todo: init gcp llm client
        pass

    async def request_answer(self, message: ChatMessage, history: ChatHistory) -> ChatAnswer:
        return ChatAnswer(output="hello world")
