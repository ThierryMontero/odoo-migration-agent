from agents.migration_rules import MigrationRules
from agents.llm.provider import LLMProvider
from agents.migration_context import MigrationContext
from agents.llm.prompt_builder import PromptBuilder
from agents.validation_agent import ValidationAgent
from agents.llm.router import ModelRouter
from agents.llm.factory import LLMProviderFactory


class MigrationAgent:

    def __init__(self, llm: LLMProvider | None = None):
        self.name = "MigrationAgent"

        self.rules = MigrationRules()

        # LLM injecté manuellement pour les tests.
        # Si None, le provider sera sélectionné via Router + Factory.
        self.llm = llm

        self.provider_factory = LLMProviderFactory()
        self.router = ModelRouter()

        self.context_builder = MigrationContext()
        self.prompt_builder = PromptBuilder()
        self.validator = ValidationAgent()

    def create_plan(
        self,
        report,
        database_report=None,
        data_report=None,
    ) -> dict:

        data = report.to_dict()

        plan = []

        # ==========================================================
        # Migration findings
        # ==========================================================

        for finding in data["migration_findings"]:

            evaluation = self.rules.evaluate(finding)

            model_config = None
            llm_result = None
            validation_result = None

            # ------------------------------------------------------
            # Router : Finding -> ModelConfig
            # ------------------------------------------------------

            if evaluation["requires_llm"]:
                model_config = self.router.route(finding)

                # --------------------------------------------------
                # 1. Construire le contexte ciblé
                # --------------------------------------------------

                context = self.context_builder.build(
                    report,
                    finding,
                    database_report=database_report,
                    data_report=data_report,
                )

                # --------------------------------------------------
                # 2. Construire le prompt
                # --------------------------------------------------

                prompt = self.prompt_builder.build(context)

                # --------------------------------------------------
                # 3. Sélectionner le provider LLM
                #
                # Si un LLM est injecté :
                #     utiliser celui-ci.
                #
                # Sinon :
                #     utiliser ModelConfig + Factory.
                # --------------------------------------------------

                if self.llm is not None:
                    provider = self.llm
                else:
                    provider = self.provider_factory.create(
                        model_config
                    )

                # --------------------------------------------------
                # 4. Appeler le LLM
                # --------------------------------------------------

                llm_result = provider.analyze(
                    context,
                    prompt,
                )

                # --------------------------------------------------
                # 5. Valider la réponse du LLM
                # --------------------------------------------------

                validation_result = self.validator.validate(
                    llm_result
                )

                # --------------------------------------------------
                # Fallback si la validation échoue
                # --------------------------------------------------

                if not validation_result["valid"]:
                    llm_result = {
                        "decision": "unknown",
                        "risk": "high",
                        "reason": (
                            "La réponse du LLM a échoué "
                            "à la validation."
                        ),
                        "recommendation": (
                            "Une analyse humaine est requise."
                        ),
                        "confidence": 0.0,
                    }

            # ------------------------------------------------------
            # Ajouter l'étape au plan
            # ------------------------------------------------------

            plan.append({
                "priority": evaluation["priority"],
                "category": evaluation["category"],
                "action": evaluation["action"],
                "requires_llm": evaluation["requires_llm"],
                "finding": finding["message"],
                "model_config": (
                    model_config.__dict__
                    if model_config is not None
                    else None
                ),
                "llm_result": llm_result,
                "validation": validation_result,
            })

        # ==========================================================
        # Cross findings
        # ==========================================================

        for finding in data["cross_findings"]:

            evaluation = self.rules.evaluate(finding)

            plan.append({
                "priority": evaluation["priority"],
                "category": evaluation["category"],
                "action": evaluation["action"],
                "requires_llm": evaluation["requires_llm"],
                "finding": finding["message"],
                "llm_result": None,
                "validation": None,
            })

        # ==========================================================
        # Trier les étapes par priorité
        # ==========================================================

        plan.sort(
            key=lambda item: item["priority"]
        )

        # ==========================================================
        # Résultat final
        # ==========================================================

        return {
            "agent": self.name,
            "module": data["module"],
            "steps": plan,
        }
