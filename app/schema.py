from pydantic import BaseModel, field_validator

MAX_INPUT_LEN = 10_000


class ChatMessageRequest(BaseModel):
    user_id: str
    session_id: str
    input: str

    @field_validator("input")
    @classmethod
    def validate_input(cls, input: str) -> str:
        if len(input) > MAX_INPUT_LEN:
            raise ValueError(f"input max len must be <= {MAX_INPUT_LEN}")
        return input


class ChatAnswerResponse(BaseModel):
    output: str
