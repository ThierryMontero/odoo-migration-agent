class ValidationAgent:

    def __init__(self):

        self.name = "ValidationAgent"

        self.allowed_decisions = {
            "compatible",
            "change_required",
            "review",
            "unknown",
        }

        self.allowed_risks = {
            "low",
            "medium",
            "high",
        }

    def validate(
        self,
        llm_result: dict,
    ) -> dict:

        errors = []

        # ==========================================
        # STRUCTURE
        # ==========================================

        required_fields = {
            "decision",
            "risk",
            "reason",
            "recommendation",
            "confidence",
        }

        missing_fields = (
            required_fields
            - llm_result.keys()
        )

        if missing_fields:

            errors.append(
                "Champs manquants : "
                + ", ".join(
                    sorted(missing_fields)
                )
            )

        # ==========================================
        # DECISION
        # ==========================================

        decision = llm_result.get(
            "decision"
        )

        if decision not in self.allowed_decisions:

            errors.append(
                f"Decision invalide : {decision}"
            )

        # ==========================================
        # RISK
        # ==========================================

        risk = llm_result.get("risk")

        if risk not in self.allowed_risks:

            errors.append(
                f"Risk invalide : {risk}"
            )

        # ==========================================
        # TEXT FIELDS
        # ==========================================

        reason = llm_result.get("reason")

        if not isinstance(reason, str) or not reason.strip():

            errors.append(
                "Reason doit être un texte non vide."
            )

        recommendation = llm_result.get(
            "recommendation"
        )

        if (
            not isinstance(
                recommendation,
                str,
            )
            or not recommendation.strip()
        ):

            errors.append(
                "Recommendation doit être "
                "un texte non vide."
            )

        # ==========================================
        # CONFIDENCE
        # ==========================================

        confidence = llm_result.get(
            "confidence"
        )

        if not isinstance(
            confidence,
            (int, float),
        ):

            errors.append(
                "Confidence doit être "
                "un nombre."
            )

        elif not 0 <= confidence <= 1:

            errors.append(
                "Confidence doit être comprise "
                "entre 0 et 1."
            )

        # ==========================================
        # RESULT
        # ==========================================

        if errors:

            return {
                "valid": False,
                "errors": errors,
            }

        return {
            "valid": True,
            "errors": [],
        }
