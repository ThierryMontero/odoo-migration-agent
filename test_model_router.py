from agents.llm.router import ModelRouter
from agents.llm.model_config import ModelConfig


def test_route_api():

    router = ModelRouter()

    result = router.route({
        "type": "api",
        "severity": "info",
        "message": "Test",
    })

    assert isinstance(result, ModelConfig)
    assert result.model == "cheap"
    assert result.provider == "openrouter"


def test_route_model():

    router = ModelRouter()

    result = router.route({
        "type": "model",
        "severity": "info",
        "message": "Test",
    })

    assert isinstance(result, ModelConfig)
    assert result.model == "standard"
    assert result.provider == "openrouter"


def test_route_wizard():

    router = ModelRouter()

    result = router.route({
        "type": "wizard",
        "severity": "warning",
        "message": "Test",
    })

    assert isinstance(result, ModelConfig)
    assert result.model == "standard"
    assert result.provider == "openrouter"


def test_route_relation():

    router = ModelRouter()

    result = router.route({
        "type": "relation",
        "severity": "warning",
        "message": "Test",
    })

    assert isinstance(result, ModelConfig)
    assert result.model == "standard"
    assert result.provider == "openrouter"


def test_route_unknown():

    router = ModelRouter()

    result = router.route({
        "type": "something_unknown",
        "severity": "high",
        "message": "Test",
    })

    assert isinstance(result, ModelConfig)
    assert result.model == "powerful"
    assert result.provider == "openrouter"


def test_route_missing_field():

    router = ModelRouter()

    result = router.route({
        "type": "missing_field",
        "severity": "high",
        "message": "Test",
    })

    assert isinstance(result, ModelConfig)
    assert result.model == "powerful"
    assert result.provider == "openrouter"