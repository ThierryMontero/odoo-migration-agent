class MigrationAnalyzer:

    def analyze_python(self, analysis: dict) -> list[dict]:
        """
        Analyse les résultats du CodeAnalyzer
        et identifie les éléments à vérifier
        lors d'une migration Odoo.
        """

        findings = []

        for model in analysis["models"]:

            findings.append({
                "type": "model",
                "severity": "info",
                "message": (
                    f"Modèle Odoo détecté : {model}"
                ),
            })

        for model_type in analysis["model_types"]:

            if model_type == "models.TransientModel":

                findings.append({
                    "type": "wizard",
                    "severity": "info",
                    "message": (
                        "Wizard Odoo détecté. "
                        "Vérifier sa compatibilité avec Odoo 19."
                    ),
                })

        for field in analysis["fields"]:

            field_name, field_type = field.split(": ")

            if field_type in {
                "Many2one",
                "One2many",
                "Many2many",
            }:

                findings.append({
                    "type": "relation",
                    "severity": "info",
                    "message": (
                        f"Relation détectée : "
                        f"{field_name} ({field_type})"
                    ),
                })

        for decorator in analysis["api_decorators"]:

            findings.append({
                "type": "api",
                "severity": "warning",
                "message": (
                    f"Décorateur API détecté : "
                    f"@api.{decorator}. "
                    "Vérifier son comportement en Odoo 19."
                ),
            })

        return findings
