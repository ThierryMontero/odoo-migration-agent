from agents.llm.model_config import ModelConfig


class ModelRouter:

    def route(self, finding: dict) -> ModelConfig:
        finding_type = finding["type"]

        if finding_type == "api":
            return ModelConfig(
                provider="openrouter",
                model="cheap",
                temperature=0.0,
            )

        if finding_type in {
            "model",
            "wizard",
            "relation",
        }:
            return ModelConfig(
                provider="openrouter",
                model="standard",
                temperature=0.0,
            )

        return ModelConfig(
            provider="openrouter",
            model="powerful",
            temperature=0.0,
        )