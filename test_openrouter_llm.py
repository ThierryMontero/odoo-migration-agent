import pytest

from agents.llm.openrouter_llm import OpenRouterLLM
from agents.llm.model_config import ModelConfig


class FakeCompletions:

    def __init__(self, response):
        self.response = response
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs
        return self.response


class FakeChat:

    def __init__(self, response):
        self.completions = FakeCompletions(response)


class FakeClient:

    def __init__(self, response):
        self.chat = FakeChat(response)


def create_llm(response):

    client = FakeClient(response)

    return OpenRouterLLM(
        model="test-model",
        api_key="fake-key",
        client=client,
    )


def valid_response():

    content = (
        '{'
        '"decision": "review", '
        '"risk": "medium", '
        '"reason": "Le modèle doit être vérifié.", '
        '"recommendation": "Comparer avec Odoo 19.", '
        '"confidence": 0.85'
        '}'
    )

    return {
        "choices": [
            {
                "message": {
                    "content": content
                }
            }
        ]
    }


def test_valid_json():

    llm = create_llm(valid_response())

    result = llm.analyze(
        context={},
        prompt="Test prompt",
    )

    assert result["decision"] == "review"
    assert result["risk"] == "medium"
    assert result["confidence"] == 0.85


def test_markdown_json():

    content = (
        "```json\n"
        "{\n"
        '    "decision": "review",\n'
        '    "risk": "medium",\n'
        '    "reason": "Test",\n'
        '    "recommendation": "Test",\n'
        '    "confidence": 0.80\n'
        "}\n"
        "```"
    )

    response = {
        "choices": [
            {
                "message": {
                    "content": content
                }
            }
        ]
    }

    llm = create_llm(response)

    result = llm.analyze(
        context={},
        prompt="Test prompt",
    )

    assert result["decision"] == "review"
    assert result["confidence"] == 0.80


def test_invalid_json():

    response = {
        "choices": [
            {
                "message": {
                    "content": "{ INVALID JSON }"
                }
            }
        ]
    }

    llm = create_llm(response)

    with pytest.raises(
        ValueError,
        match="JSON incorrect",
    ):
        llm.analyze(
            context={},
            prompt="Test prompt",
        )


def test_empty_response():

    response = {
        "choices": [
            {
                "message": {
                    "content": ""
                }
            }
        ]
    }

    llm = create_llm(response)

    with pytest.raises(
        ValueError,
        match="contenu vide",
    ):
        llm.analyze(
            context={},
            prompt="Test prompt",
        )


def test_missing_choices():

    llm = create_llm({})

    with pytest.raises(
        ValueError,
        match="choices",
    ):
        llm.analyze(
            context={},
            prompt="Test prompt",
        )


def test_missing_message():

    response = {
        "choices": [
            {}
        ]
    }

    llm = create_llm(response)

    with pytest.raises(
        ValueError,
        match="message",
    ):
        llm.analyze(
            context={},
            prompt="Test prompt",
        )


def test_missing_content():

    response = {
        "choices": [
            {
                "message": {}
            }
        ]
    }

    llm = create_llm(response)

    with pytest.raises(
        ValueError,
        match="content",
    ):
        llm.analyze(
            context={},
            prompt="Test prompt",
        )

def test_request_parameters():

    response = valid_response()

    client = FakeClient(response)

    llm = OpenRouterLLM(
        model="test-model",
        api_key="fake-key",
        temperature=0.2,
        max_tokens=500,
        client=client,
    )

    llm.analyze(
        context={},
        prompt="Test prompt",
    )

    request = client.chat.completions.last_request

    assert request["model"] == "test-model"
    assert request["temperature"] == 0.2
    assert request["max_tokens"] == 500

    assert request["messages"] == [
        {
            "role": "user",
            "content": "Test prompt",
        }
    ]

def test_api_key_from_environment(monkeypatch):

    monkeypatch.setenv(
        "OPENROUTER_API_KEY",
        "env-test-key",
    )

    llm = OpenRouterLLM(
        client=FakeClient(valid_response()),
    )

    assert llm.api_key == "env-test-key"

def test_create_client():

    llm = OpenRouterLLM(
        api_key="fake-openrouter-key",
    )

    client = llm._create_client()

    assert client.api_key == "fake-openrouter-key"
    assert str(client.base_url).rstrip("/") == \
        "https://openrouter.ai/api/v1"


def test_create_client_without_api_key(monkeypatch):

    monkeypatch.delenv(
        "OPENROUTER_API_KEY",
        raising=False,
    )

    llm = OpenRouterLLM()

    with pytest.raises(
        RuntimeError,
        match="OPENROUTER_API_KEY",
    ):
        llm._create_client()

def test_openrouter_llm_with_model_config():

    config = ModelConfig(
        provider="openrouter",
        model="test-config-model",
        temperature=0.3,
        max_tokens=750,
        api_key="config-test-key",
        base_url="https://openrouter.example/api/v1",
    )

    client = FakeClient(valid_response())

    llm = OpenRouterLLM(
        config=config,
        client=client,
    )

    assert llm.model == "test-config-model"
    assert llm.temperature == 0.3
    assert llm.max_tokens == 750
    assert llm.api_key == "config-test-key"
    assert llm.config is config