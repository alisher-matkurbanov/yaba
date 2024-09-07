from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.handler.schema import ChatMessageRequest

client = TestClient(app)


@pytest.fixture
def user_id():
    return "95f3a66c-f6f2-4767-90da-3c4934058acc"


@pytest.fixture
def session_id():
    return "79db3503-ff58-4ec4-850d-1e371548eae4"


@pytest.fixture
def chat_request(user_id, session_id):
    return ChatMessageRequest(
        user_id=user_id,
        session_id=session_id,
        input="test prompt"
    )


def test_handle_chat(chat_request):
    response = client.post(
        "/chat",
        content=chat_request.model_dump_json(),
        headers={
            "Idempotency-Key": str(uuid4())
        })
    assert response.status_code == 200, response.json()
    assert response.json() == {"output": "hello world"}
