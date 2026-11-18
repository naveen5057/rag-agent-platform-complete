import pytest
from pydantic import ValidationError
from agent_service_schema import AgentRequest


def test_agent_request_schema():
    assert AgentRequest(question="hello").question == "hello"


def test_empty_question_rejected():
    with pytest.raises(ValidationError):
        AgentRequest(question="")


def test_oversized_question_rejected():
    with pytest.raises(ValidationError):
        AgentRequest(question="x" * 4001)
