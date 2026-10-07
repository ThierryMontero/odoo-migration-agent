from agents.context_selector import ContextSelector


class FakeReport:
    def to_dict(self):
        return {
            "module": "examples/cartin_refund",
            "manifest": {
                "version": "16.0.1.0.0",
            },
            "python": [
                {
                    "file": "models/refund.py",
                    "analysis": {
                        "classes": ["CartinRefund"],
                        "models": ["cartin.refund"],
                        "model_types": ["models.Model"],
                        "descriptions": ["Cartin Refund"],
                        "fields": [
                            "name: Char",
                            "amount: Float",
                            "state: Selection",
                        ],
                        "api_decorators": ["model"],
                    },
                },
                {
                    "file": "wizard/refund_wizard.py",
                    "analysis": {
                        "classes": ["CartinRefundWizard"],
                        "models": ["cartin.refund.wizard"],
                        "model_types": ["models.TransientModel"],
                        "descriptions": [],
                        "fields": [
                            "refund_id: Many2one",
                        ],
                        "api_decorators": [],
                    },
                },
                {
                    "file": "models/other.py",
                    "analysis": {
                        "classes": ["OtherModel"],
                        "models": ["other.model"],
                        "model_types": ["models.Model"],
                        "descriptions": [],
                        "fields": [
                            "name: Char",
                        ],
                        "api_decorators": [],
                    },
                },
            ],
            "xml": [
                {
                    "file": "views/refund_views.xml",
                    "analysis": {
                        "views": ["cartin.refund.form"],
                    },
                }
            ],
        }


report = FakeReport()
selector = ContextSelector()


# ============================================================
# TEST 1 — API
# ============================================================

api_finding = {
    "type": "api",
    "severity": "warning",
    "message": (
        "Décorateur API détecté : "
        "@api.model. Vérifier son comportement en Odoo 19."
    ),
}

api_context = selector.select(report, api_finding)

assert len(api_context["python"]) == 1
assert api_context["python"][0]["file"] == "models/refund.py"

print("API : OK")


# ============================================================
# TEST 2 — MODEL
# ============================================================

model_finding = {
    "type": "model",
    "severity": "info",
    "message": "Modèle Odoo détecté : cartin.refund",
}

model_context = selector.select(report, model_finding)

assert len(model_context["python"]) == 1
assert model_context["python"][0]["file"] == "models/refund.py"

print("MODEL : OK")


# ============================================================
# TEST 3 — WIZARD
# ============================================================

wizard_finding = {
    "type": "wizard",
    "severity": "info",
    "message": (
        "Wizard Odoo détecté. "
        "Vérifier sa compatibilité avec Odoo 19."
    ),
}

wizard_context = selector.select(report, wizard_finding)

assert len(wizard_context["python"]) == 1
assert (
    wizard_context["python"][0]["file"]
    == "wizard/refund_wizard.py"
)

print("WIZARD : OK")


# ============================================================
# TEST 4 — RELATION
# ============================================================

relation_finding = {
    "type": "relation",
    "severity": "info",
    "message": "Relation détectée : refund_id (Many2one)",
}

relation_context = selector.select(
    report,
    relation_finding,
)

assert len(relation_context["python"]) == 1
assert (
    relation_context["python"][0]["file"]
    == "wizard/refund_wizard.py"
)

print("RELATION : OK")


# ============================================================
# TEST 5 — UNKNOWN
# ============================================================

unknown_finding = {
    "type": "unknown",
    "severity": "info",
    "message": "Finding inconnu",
}

unknown_context = selector.select(
    report,
    unknown_finding,
)

assert len(unknown_context["python"]) == 3
assert len(unknown_context["xml"]) == 1

print("UNKNOWN : OK")


# ============================================================
# TEST 6 — INFORMATIONS COMMUNES
# ============================================================

assert api_context["module"] == "examples/cartin_refund"
assert api_context["source_version"] == "16.0.1.0.0"
assert api_context["target_version"] == "19.0"
assert api_context["finding"] == api_finding

print("COMMON CONTEXT : OK")


print("\nContextSelector : VALID")
