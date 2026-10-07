import pytest

from agents.llm.factory import LLMProviderFactory
from agents.llm.model_config import ModelConfig
from agents.llm.mock import MockLLM
from agents.llm.openrouter_llm import OpenRouterLLM


def test_create_mock_provider():
    config = ModelConfig(
        provider="mock",
        model="test-model",
    )

    provider = LLMProviderFactory.create(config)

    assert isinstance(provider, MockLLM)


def test_create_openrouter_provider():
    config = ModelConfig(
        provider="openrouter",
        model="test-model",
        api_key="fake-key",
    )

    provider = LLMProviderFactory.create(config)

    assert isinstance(provider, OpenRouterLLM)
    assert provider.model == "test-model"
    assert provider.api_key == "fake-key"


def test_unknown_provider():
    config = ModelConfig(
        provider="unknown",
        model="test-model",
    )

    with pytest.raises(ValueError, match="Provider LLM inconnu"):
        LLMProviderFactory.create(config)
