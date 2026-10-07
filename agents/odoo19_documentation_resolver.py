class Odoo19DocumentationResolver:
    """
    Résout des fonctionnalités vers des références connues
    de la documentation officielle Odoo 19.

    V1 :
    - catalogue statique ;
    - aucune recherche web dynamique ;
    - aucune décision de migration ;
    - retourne une preuve documentaire structurée.
    """

    BASE_URL = "https://www.odoo.com/documentation/19.0"

    DOCUMENTATION = {
        "computed_field": {
            "title": "Computed Fields",
            "category": "ORM",
            "version": "19.0",
            "url": (
                f"{BASE_URL}/developer/reference/backend/orm.html"
            ),
            "evidence": (
                "Odoo 19 ORM documentation describes computed fields."
            ),
            "confidence": 0.95,
        },
        "view_inheritance": {
            "title": "View inheritance",
            "category": "Views",
            "version": "19.0",
            "url": (
                f"{BASE_URL}/developer/reference/"
                "user_interface/view_records.html"
            ),
            "evidence": (
                "Odoo 19 documents inherited views and view inheritance."
            ),
            "confidence": 0.95,
        },
        "window_action": {
            "title": "Window Actions",
            "category": "Actions",
            "version": "19.0",
            "url": (
                f"{BASE_URL}/developer/reference/backend/actions.html"
            ),
            "evidence": (
                "Odoo 19 documents window actions."
            ),
            "confidence": 0.95,
        },
    }

    def resolve(self, feature: str) -> dict:
        documentation = self.DOCUMENTATION.get(feature)

        if documentation is None:
            return {
                "status": "UNCERTAIN",
                "documentation": None,
                "confidence": 0.0,
            }

        return {
            "status": "NATIVE_FOUND",
            "documentation": documentation,
            "confidence": documentation["confidence"],
        }
