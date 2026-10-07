class FunctionalAnalyzer:
    """
    Analyse fonctionnelle déterministe d'un module Odoo.

    V1 :
    - identifie le modèle principal ;
    - regroupe les éléments représentant du comportement custom ;
    - conserve les éléments techniques détectés.
    """

    def analyze(
        self,
        code_analysis: dict,
        xml_analysis: dict,
        manifest: dict | None = None,
    ) -> dict:

        inherits = code_analysis.get("inherits", [])
        models = code_analysis.get("models", [])

        # Priorité au modèle hérité, car il représente souvent
        # la cible fonctionnelle principale du custom.
        model = inherits[0] if inherits else (
            models[0] if models else None
        )

        # Si aucun modèle n'est trouvé dans le Python,
        # chercher le modèle fonctionnel dans les vues XML.
        if model is None:
            for view in xml_analysis.get("views", []):
                view_model = view.get("model")
                if view_model:
                    model = view_model
                    break

        fields = code_analysis.get("fields", [])
        methods = code_analysis.get("methods", [])

        views = xml_analysis.get("views", [])
        xpaths = []

        for view in views:
            xpaths.extend(view.get("xpaths", []))

        actions = xml_analysis.get("actions", [])
        reports = xml_analysis.get("reports", [])
        menus = xml_analysis.get("menus", [])

        custom_behavior = []

        # Champs custom
        for field in fields:
            field_name = field.split(":", 1)[0].strip()
            if field_name:
                custom_behavior.append(field_name)

        # Méthodes custom
        custom_behavior.extend(methods)

        # Vues custom
        for view in views:
            view_id = view.get("id")
            if view_id:
                custom_behavior.append(view_id)

        technical_elements = {
            "fields": fields,
            "methods": methods,
            "views": views,
            "xpaths": xpaths,
            "actions": actions,
            "reports": reports,
            "menus": menus,
        }

        return {
            "type": "functional_analysis",
            "model": model,
            "custom_behavior": custom_behavior,
            "technical_elements": technical_elements,
            "manifest": manifest or {},
        }
