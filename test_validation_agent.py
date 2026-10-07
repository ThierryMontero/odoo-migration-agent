from agents.validation_agent import ValidationAgent


validator = ValidationAgent()


# ============================================================
# TEST 1 — Réponse valide
# ============================================================

valid_result = {
    "decision": "review",
    "risk": "medium",
    "reason": "Analyse nécessaire.",
    "recommendation": "Vérifier la compatibilité.",
    "confidence": 0.8,
}

result = validator.validate(valid_result)

assert result["valid"] is True
assert result["errors"] == []

print("VALID RESPONSE : OK")


# ============================================================
# TEST 2 — Champ manquant
# ============================================================

missing_field = {
    "decision": "review",
    "risk": "medium",
    "reason": "Analyse nécessaire.",
    "confidence": 0.8,
}

result = validator.validate(missing_field)

assert result["valid"] is False
assert any(
    "Champs manquants" in error
    for error in result["errors"]
)

print("MISSING FIELD : OK")


# ============================================================
# TEST 3 — Decision invalide
# ============================================================

invalid_decision = {
    "decision": "maybe",
    "risk": "medium",
    "reason": "Analyse nécessaire.",
    "recommendation": "Vérifier.",
    "confidence": 0.8,
}

result = validator.validate(invalid_decision)

assert result["valid"] is False

print("INVALID DECISION : OK")


# ============================================================
# TEST 4 — Risk invalide
# ============================================================

invalid_risk = {
    "decision": "review",
    "risk": "critical",
    "reason": "Analyse nécessaire.",
    "recommendation": "Vérifier.",
    "confidence": 0.8,
}

result = validator.validate(invalid_risk)

assert result["valid"] is False

print("INVALID RISK : OK")


# ============================================================
# TEST 5 — Confidence > 1
# ============================================================

confidence_high = {
    "decision": "review",
    "risk": "medium",
    "reason": "Analyse nécessaire.",
    "recommendation": "Vérifier.",
    "confidence": 1.5,
}

result = validator.validate(confidence_high)

assert result["valid"] is False

print("CONFIDENCE > 1 : OK")


# ============================================================
# TEST 6 — Confidence < 0
# ============================================================

confidence_low = {
    "decision": "review",
    "risk": "medium",
    "reason": "Analyse nécessaire.",
    "recommendation": "Vérifier.",
    "confidence": -0.1,
}

result = validator.validate(confidence_low)

assert result["valid"] is False

print("CONFIDENCE < 0 : OK")


# ============================================================
# TEST 7 — Reason vide
# ============================================================

empty_reason = {
    "decision": "review",
    "risk": "medium",
    "reason": "",
    "recommendation": "Vérifier.",
    "confidence": 0.8,
}

result = validator.validate(empty_reason)

assert result["valid"] is False

print("EMPTY REASON : OK")


# ============================================================
# TEST 8 — Recommendation vide
# ============================================================

empty_recommendation = {
    "decision": "review",
    "risk": "medium",
    "reason": "Analyse nécessaire.",
    "recommendation": "",
    "confidence": 0.8,
}

result = validator.validate(empty_recommendation)

assert result["valid"] is False

print("EMPTY RECOMMENDATION : OK")


print("\nValidationAgent : VALID")
