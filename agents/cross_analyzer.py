class CrossAnalyzer:

    def compare_model_and_view(
        self,
        python_analysis: dict,
        xml_view: dict,
    ) -> list[dict]:

        findings = []

        # ==========================================
        # MODÈLE
        # ==========================================

        python_models = python_analysis.get(
            "models",
            []
        )

        xml_model = xml_view.get(
            "model"
        )

        if xml_model not in python_models:

            findings.append({
                "type": "missing_model",
                "severity": "error",
                "message": (
                    f"La vue référence le modèle "
                    f"'{xml_model}', mais ce modèle "
                    f"n'a pas été trouvé dans le Python."
                ),
            })

            return findings

        # ==========================================
        # CHAMPS PYTHON
        # ==========================================

        python_fields = set()

        for field in python_analysis.get(
            "fields",
            []
        ):

            field_name = field.split(":")[0]

            python_fields.add(
                field_name
            )

        # ==========================================
        # CHAMPS XML
        # ==========================================

        xml_fields = xml_view.get(
            "fields",
            []
        )

        for field_name in xml_fields:

            if field_name not in python_fields:

                findings.append({
                    "type": "missing_field",
                    "severity": "error",
                    "message": (
                        f"Le champ '{field_name}' "
                        f"est utilisé dans la vue "
                        f"'{xml_view['id']}', mais "
                        f"n'existe pas dans le modèle "
                        f"'{xml_model}'."
                    ),
                })

        return findings