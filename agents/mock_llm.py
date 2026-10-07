class MockLLM:

    def __init__(self):

        self.name = "MockLLM"

    def analyze(
        self,
        finding: dict,
    ) -> dict:

        finding_type = finding["type"]

        if finding_type == "api":

            return {
                "decision": "review",
                "reason": (
                    "Le décorateur API doit être "
                    "analysé dans son contexte "
                    "avant de déterminer s'il "
                    "nécessite une modification."
                ),
            }

        if finding_type == "model":

            return {
                "decision": "review",
                "reason": (
                    "Le modèle doit être comparé "
                    "aux changements de structure "
                    "entre les versions Odoo."
                ),
            }

        if finding_type == "wizard":

            return {
                "decision": "review",
                "reason": (
                    "Le wizard doit être inspecté "
                    "pour vérifier ses méthodes, "
                    "vues et interactions."
                ),
            }

        if finding_type == "relation":

            return {
                "decision": "review",
                "reason": (
                    "La relation doit être vérifiée "
                    "avec le modèle cible."
                ),
            }

        return {
            "decision": "manual_review",
            "reason": (
                "Analyse manuelle recommandée."
            ),
        }
