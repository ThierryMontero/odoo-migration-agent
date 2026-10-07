from dataclasses import dataclass


@dataclass
class ModelConfig:
    """
    Configuration d'un modèle LLM.
    """

    provider: str
    model: str
    temperature: float = 0.0
    max_tokens: int | None = None
    api_key: str | None = None
    base_url: str | None = None
