from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def analyze(
        self,
        context: dict,
        prompt: str,
    ) -> dict:
        """
        Analyse un contexte à partir d'un prompt
        et retourne une recommandation structurée.
        """
        raise NotImplementedError