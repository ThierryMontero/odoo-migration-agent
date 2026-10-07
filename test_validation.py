from agents.validation_agent import ValidationAgent


validator = ValidationAgent()


valid_result = {
    "decision": "review",
    "risk": "low",
    "reason": "La relation doit être vérifiée.",
    "recommendation": (
        "Vérifier le modèle cible."
    ),
    "confidence": 0.9,
}


invalid_result = {
    "decision": "foobar",
    "risk": "extreme",
    "reason": "",
    "recommendation": "",
    "confidence": 2,
}


print("===== VALID RESULT =====")

print(
    validator.validate(
        valid_result
    )
)


print("\n===== INVALID RESULT =====")

print(
    validator.validate(
        invalid_result
    )
)
