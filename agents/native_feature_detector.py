class NativeFeatureDetector:
    """
    Prépare les éléments fonctionnels custom qui devront être
    comparés aux fonctionnalités natives d'Odoo 19.

    V1 :
    - ne consulte pas encore la documentation Odoo ;
    - ne prend aucune décision de migration ;
    - extrait uniquement les fonctionnalités candidates.
    """

    def detect(self, functional_analysis: dict) -> dict:
        technical_elements = functional_analysis.get(
            "technical_elements",
            {}
        )

        features = []

        # Champs
        for field in technical_elements.get("fields", []):
            name = field.split(":", 1)[0].strip()

            if name:
                features.append({
                    "type": "field",
                    "name": name,
                    "source": "custom",
                })

        # Méthodes
        for method in technical_elements.get("methods", []):
            features.append({
                "type": "method",
                "name": method,
                "source": "custom",
            })

        # Vues
        for view in technical_elements.get("views", []):
            view_id = view.get("id")

            if view_id:
                features.append({
                    "type": "view",
                    "name": view_id,
                    "source": "custom",
                })

        # Actions
        for action in technical_elements.get("actions", []):
            features.append({
                "type": "action",
                "name": action,
                "source": "custom",
            })

        # Rapports
        for report in technical_elements.get("reports", []):
            report_id = report.get("id")

            if report_id:
                features.append({
                    "type": "report",
                    "name": report_id,
                    "source": "custom",
                })

        # Menus
        for menu in technical_elements.get("menus", []):
            menu_id = menu.get("id")

            if menu_id:
                features.append({
                    "type": "menu",
                    "name": menu_id,
                    "source": "custom",
                })

        return {
            "type": "native_feature_candidates",
            "model": functional_analysis.get("model"),
            "features": features,
        }
