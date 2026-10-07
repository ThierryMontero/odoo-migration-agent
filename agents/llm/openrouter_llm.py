import os
import json
from openai import OpenAI

from agents.llm.provider import LLMProvider
from agents.llm.model_config import ModelConfig


class OpenRouterLLM(LLMProvider):

    def __init__(
        self,
        model: str = "openai/gpt-4o-mini",
        api_key: str | None = None,
        client=None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        config: ModelConfig | None = None,
    ):
        if config is None:
            config = ModelConfig(
                provider="openrouter",
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
            )

        self.config = config

        self.name = "OpenRouterLLM"
        self.model = config.model
        self.api_key = config.api_key
        self.client = client
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    def _create_client(self):
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY n'est pas configurée."
            )

        return OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def _parse_json_response(self, content: str) -> dict:
        """
        Nettoie et parse la réponse JSON du LLM.

        Accepte :
        - JSON pur
        - JSON entouré de ```json ... ```
        - JSON entouré de ``` ... ```
        """

        content = content.strip()

        if not content:
            raise ValueError(
                "Réponse LLM invalide : contenu vide."
            )

        if content.startswith("```json"):
            content = content[7:]

        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Réponse LLM invalide : JSON incorrect. "
                f"Détail : {exc}"
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "Réponse LLM invalide : "
                "le JSON doit être un objet."
            )

        return result

    def analyze(
        self,
        context: dict,
        prompt: str,
    ) -> dict:

        if self.client is None:
            self.client = self._create_client()

        request = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": self.temperature,
        }

        if self.max_tokens is not None:
            request["max_tokens"] = self.max_tokens

        response = self.client.chat.completions.create(
            **request
        )

        choices = response.get("choices")

        if not choices:
            raise ValueError(
                "Réponse OpenRouter invalide : "
                "champ 'choices' absent ou vide."
            )

        message = choices[0].get("message")

        if message is None:
            raise ValueError(
                "Réponse OpenRouter invalide : "
                "champ 'message' absent ou vide."
            )

        content = message.get("content")

        if content is None:
            raise ValueError(
                "Réponse OpenRouter invalide : "
                "champ 'content' absent."
            )

        return self._parse_json_response(content)

    