class GlobalValidationAgent:

    def __init__(self):

        self.name = "GlobalValidationAgent"

        self.required_step_fields = {
            "priority",
            "category",
            "action",
            "requires_llm",
            "finding",
            "llm_result",
            "validation",
        }

    def validate(
        self,
        migration_plan: dict,
    ) -> dict:

        errors = []

        # ==========================================
        # PLAN
        # ==========================================

        if not isinstance(
            migration_plan,
            dict,
        ):

            return {
                "valid": False,
                "errors": [
                    "Le migration plan doit être un dictionnaire."
                ],
            }

        # ==========================================
        # STEPS
        # ==========================================

        if "steps" not in migration_plan:

            errors.append(
                "Le migration plan ne contient pas 'steps'."
            )

            return {
                "valid": False,
                "errors": errors,
            }

        steps = migration_plan["steps"]

        if not isinstance(steps, list):

            errors.append(
                "'steps' doit être une liste."
            )

            return {
                "valid": False,
                "errors": errors,
            }

        if not steps:

            errors.append(
                "Le migration plan ne contient aucune étape."
            )

        # ==========================================
        # STEP VALIDATION
        # ==========================================

        for index, step in enumerate(
            steps,
            start=1,
        ):

            if not isinstance(step, dict):

                errors.append(
                    f"Étape {index} : "
                    "l'étape doit être un dictionnaire."
                )

                continue

            missing_fields = (
                self.required_step_fields
                - step.keys()
            )

            if missing_fields:

                errors.append(
                    f"Étape {index} : "
                    "champs manquants : "
                    + ", ".join(
                        sorted(missing_fields)
                    )
                )

                continue

            # ======================================
            # BASIC FIELDS
            # ======================================

            if not isinstance(
                step["priority"],
                int,
            ):

                errors.append(
                    f"Étape {index} : "
                    "priority doit être un entier."
                )

            if not isinstance(
                step["category"],
                str,
            ) or not step["category"].strip():

                errors.append(
                    f"Étape {index} : "
                    "category doit être un texte non vide."
                )

            if not isinstance(
                step["action"],
                str,
            ) or not step["action"].strip():

                errors.append(
                    f"Étape {index} : "
                    "action doit être un texte non vide."
                )

            if not isinstance(
                step["finding"],
                str,
            ) or not step["finding"].strip():

                errors.append(
                    f"Étape {index} : "
                    "finding doit être un texte non vide."
                )

            if not isinstance(
                step["requires_llm"],
                bool,
            ):

                errors.append(
                    f"Étape {index} : "
                    "requires_llm doit être un booléen."
                )

            # ======================================
            # LLM VALIDATION
            # ======================================

            if step["requires_llm"]:

                if step["llm_result"] is None:

                    errors.append(
                        f"Étape {index} : "
                        "une réponse LLM est requise."
                    )

                if step["validation"] is None:

                    errors.append(
                        f"Étape {index} : "
                        "le résultat de validation est requis."
                    )

                elif not step["validation"].get(
                    "valid",
                    False,
                ):

                    errors.append(
                        f"Étape {index} : "
                        "la validation du résultat LLM a échoué."
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
