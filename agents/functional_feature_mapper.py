class FunctionalFeatureMapper:
    """
    Transforme l'analyse fonctionnelle en fonctionnalités
    pouvant être comparées aux capacités natives d'Odoo 19.

    V1 :
    - règles déterministes ;
    - aucune recherche documentaire ;
    - aucune utilisation du LLM ;
    - aucun jugement de migration.
    """

    def map(self, functional_analysis: dict) -> dict:
        model = functional_analysis.get("model")

        technical_elements = functional_analysis.get(
            "technical_elements",
            {}
        )

        features = []

        fields = technical_elements.get("fields", [])
        methods = technical_elements.get("methods", [])
        views = technical_elements.get("views", [])
        actions = technical_elements.get("actions", [])

        field_metadata = technical_elements.get(
            "field_metadata",
            []
        )

        # ---------------------------------------------------------
        # Computed fields
        # ---------------------------------------------------------

        for field in field_metadata:

            compute_method = field.get("compute")

            if not compute_method:
                continue

            field_name = field.get("name")

            if not field_name:
                continue

            features.append({
                "type": "computed_field",
                "name": field_name,
                "model": model,
                "evidence": {
                    "field": field,
                    "compute_method": compute_method,
                },
            })

        # ---------------------------------------------------------
        # View inheritance
        # ---------------------------------------------------------
        for view in views:
            xpaths = view.get("xpaths", [])

            if not xpaths:
                continue

            view_id = view.get("id")

            if view_id:
                features.append({
                    "type": "view_inheritance",
                    "name": view_id,
                    "model": view.get("model") or model,
                    "evidence": {
                        "xpaths": xpaths,
                    },
                })

        # ---------------------------------------------------------
        # Window actions
        # ---------------------------------------------------------
        for action in actions:
            if isinstance(action, str):
                action_name = action
            else:
                action_name = action.get("id")

            if action_name:
                features.append({
                    "type": "window_action",
                    "name": action_name,
                    "model": model,
                })

        return {
            "type": "functional_features",
            "model": model,
            "features": features,
        }
