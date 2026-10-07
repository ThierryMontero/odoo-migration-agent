from agents.llm.model_config import ModelConfig
from agents.llm.mock import MockLLM
from agents.llm.openrouter_llm import OpenRouterLLM


class LLMProviderFactory:
    """Construit le provider LLM correspondant à une ModelConfig."""

    @staticmethod
    def create(config: ModelConfig):
        if config.provider == "mock":
            return MockLLM()

        if config.provider == "openrouter":
            return OpenRouterLLM(config=config)

        raise ValueError(
            f"Provider LLM inconnu : {config.provider}"
        )
