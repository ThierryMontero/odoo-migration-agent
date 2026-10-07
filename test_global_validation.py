from agents.global_validation_agent import GlobalValidationAgent


validator = GlobalValidationAgent()


# ==========================================
# VALID PLAN
# ==========================================

valid_plan = {
    "agent": "MigrationAgent",
    "module": "examples/cartin_refund",
    "steps": [
        {
            "priority": 2,
            "category": "api",
            "action": "Analyser le décorateur.",
            "requires_llm": True,
            "finding": "Décorateur API détecté.",
            "llm_result": {
                "decision": "review",
                "risk": "medium",
                "reason": "Analyse nécessaire.",
                "recommendation": "Vérifier la compatibilité.",
                "confidence": 0.85,
            },
            "validation": {
                "valid": True,
                "errors": [],
            },
        }
    ],
}


# ==========================================
# INVALID PLAN
# ==========================================

invalid_plan = {
    "agent": "MigrationAgent",
    "module": "examples/cartin_refund",
    "steps": [
        {
            "priority": 2,
            "category": "api",
            "action": "Analyser le décorateur.",
            "requires_llm": True,
            "finding": "Décorateur API détecté.",
            "llm_result": {
                "decision": "foobar",
            },
            "validation": {
                "valid": False,
                "errors": [
                    "Decision invalide : foobar"
                ],
            },
        }
    ],
}


# ==========================================
# TEST VALID
# ==========================================

valid_result = validator.validate(
    valid_plan
)

print("\n===== VALID PLAN =====")
print(valid_result)


# ==========================================
# TEST INVALID
# ==========================================

invalid_result = validator.validate(
    invalid_plan
)

print("\n===== INVALID PLAN =====")
print(invalid_result)
