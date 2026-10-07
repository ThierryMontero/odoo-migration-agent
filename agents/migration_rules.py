class MigrationRules:

    def evaluate(
        self,
        finding: dict,
    ) -> dict:

        finding_type = finding["type"]

        if finding_type == "model":

            return {
                "priority": 3,
                "category": "model",
                "action": (
                    "Inspecter la définition du "
                    "modèle et ses champs."
                ),
                "requires_llm": True,
            }

        if finding_type == "wizard":

            return {
                "priority": 3,
                "category": "wizard",
                "action": (
                    "Inspecter le wizard et ses "
                    "méthodes pour vérifier "
                    "sa compatibilité."
                ),
                "requires_llm": True,
            }

        if finding_type == "relation":

            return {
                "priority": 3,
                "category": "relation",
                "action": (
                    "Vérifier le modèle cible "
                    "de la relation."
                ),
                "requires_llm": True,
            }

        if finding_type == "api":

            return {
                "priority": 2,
                "category": "api",
                "action": (
                    "Analyser le contexte et "
                    "l'utilisation du décorateur."
                ),
                "requires_llm": True,
            }

        if finding_type == "missing_field":

            return {
                "priority": 1,
                "category": "xml",
                "action": (
                    "Corriger la référence "
                    "vers le champ inexistant."
                ),
                "requires_llm": False,
            }

        if finding_type == "missing_model":

            return {
                "priority": 1,
                "category": "xml",
                "action": (
                    "Corriger la référence "
                    "vers le modèle inexistant."
                ),
                "requires_llm": False,
            }

        return {
            "priority": 4,
            "category": "unknown",
            "action": (
                "Analyser manuellement."
            ),
            "requires_llm": True,
        }
