from agents.llm.provider import LLMProvider


class MockLLM(LLMProvider):

    def __init__(self):

        self.name = "MockLLM"

    def analyze(
        self,
        context: dict,
        prompt: str,
    ) -> dict:

        finding = context["finding"]
        
        print("\n===== LLM CONTEXT =====")
        print(context)

        finding_type = finding["type"]

        if finding_type == "api":

            return {
                "decision": "review",
                "risk": "medium",
                "reason": (
                    "Le décorateur API doit être "
                    "analysé dans son contexte "
                    "avant de déterminer s'il "
                    "nécessite une modification."
                ),
                "recommendation": (
                    "Vérifier l'utilisation de "
                    "@api.model et sa compatibilité "
                    "avec Odoo 19."
                ),
                "confidence": 0.85,
            }

        if finding_type == "model":

            return {
                "decision": "review",
                "risk": "medium",
                "reason": (
                    "Le modèle doit être comparé "
                    "aux changements de structure "
                    "entre les versions Odoo."
                ),
                "recommendation": (
                    "Comparer la définition du modèle "
                    "et ses champs avec les exigences "
                    "d'Odoo 19."
                ),
                "confidence": 0.80,
            }

        if finding_type == "wizard":

            return {
                "decision": "review",
                "risk": "medium",
                "reason": (
                    "Le wizard doit être inspecté "
                    "pour vérifier ses méthodes, "
                    "vues et interactions."
                ),
                "recommendation": (
                    "Vérifier la compatibilité du "
                    "TransientModel, de ses méthodes "
                    "et de ses vues avec Odoo 19."
                ),
                "confidence": 0.82,
            }

        if finding_type == "relation":

            return {
                "decision": "review",
                "risk": "low",
                "reason": (
                    "La relation doit être vérifiée "
                    "avec le modèle cible."
                ),
                "recommendation": (
                    "Vérifier que le champ relationnel "
                    "et son modèle cible restent "
                    "compatibles avec Odoo 19."
                ),
                "confidence": 0.90,
            }

        return {
            "decision": "unknown",
            "risk": "medium",
            "reason": (
                "Analyse manuelle recommandée."
            ),
            "recommendation": (
                "Effectuer une analyse manuelle "
                "avant toute modification."
            ),
            "confidence": 0.50,
        }