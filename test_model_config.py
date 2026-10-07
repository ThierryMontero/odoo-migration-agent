from agents.llm.model_config import ModelConfig


def test_model_config_defaults():

    config = ModelConfig(
        provider="openrouter",
        model="test-model",
    )

    assert config.provider == "openrouter"
    assert config.model == "test-model"
    assert config.temperature == 0.0
    assert config.max_tokens is None
    assert config.api_key is None
    assert config.base_url is None


def test_model_config_custom_values():

    config = ModelConfig(
        provider="openrouter",
        model="test-model",
        temperature=0.2,
        max_tokens=500,
        api_key="fake-key",
        base_url="https://example.com",
    )

    assert config.provider == "openrouter"
    assert config.model == "test-model"
    assert config.temperature == 0.2
    assert config.max_tokens == 500
    assert config.api_key == "fake-key"
    assert config.base_url == "https://example.com"
