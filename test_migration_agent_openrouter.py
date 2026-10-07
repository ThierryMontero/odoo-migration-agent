from agents.migration_agent import MigrationAgent
from agents.llm.openrouter_llm import OpenRouterLLM


class FakeReport:

    def __init__(self):
        self.module = "examples/cartin_refund"

    def to_dict(self):
        return {
            "module": self.module,
            "manifest": {},
            "python": [],
            "xml": [],
            "migration_findings": [
                {
                    "type": "model",
                    "severity": "info",
                    "message": "Modèle Odoo détecté : cartin.refund",
                },
                {
                    "type": "api",
                    "severity": "warning",
                    "message": "Décorateur API détecté : @api.model.",
                },
                {
                    "type": "wizard",
                    "severity": "info",
                    "message": "Wizard Odoo détecté.",
                },
                {
                    "type": "relation",
                    "severity": "info",
                    "message": "Relation détectée : refund_id.",
                },
                {
                    "type": "model",
                    "severity": "info",
                    "message": "Modèle Odoo détecté : cartin.refund.wizard",
                },
            ],
            "cross_findings": [],
        }


class FakeCompletions:

    def create(self, **kwargs):

        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{'
                            '"decision": "review", '
                            '"risk": "medium", '
                            '"reason": "Analyse réalisée par le Fake OpenRouter.", '
                            '"recommendation": "Vérifier la compatibilité avec Odoo 19.", '
                            '"confidence": 0.90'
                            '}'
                        )
                    }
                }
            ]
        }


class FakeChat:

    def __init__(self):
        self.completions = FakeCompletions()


class FakeClient:

    def __init__(self):
        self.chat = FakeChat()


def test_migration_agent_with_openrouter():

    report = FakeReport()

    fake_client = FakeClient()

    llm = OpenRouterLLM(
        model="test-model",
        api_key="fake-key",
        client=fake_client,
    )

    agent = MigrationAgent(llm=llm)

    plan = agent.create_plan(report)

    assert plan["agent"] == "MigrationAgent"

    assert plan["module"] == "examples/cartin_refund"

    assert len(plan["steps"]) == 5

    for step in plan["steps"]:

        assert step["llm_result"] is not None

        assert step["validation"] is not None

        assert step["validation"]["valid"] is True

        assert step["llm_result"]["decision"] == "review"

        assert step["llm_result"]["risk"] == "medium"

        assert step["llm_result"]["confidence"] == 0.90

def test_migration_agent_uses_provider_factory(monkeypatch):
    class FakeProvider:
        def analyze(self, context, prompt):
            return {
                "decision": "review",
                "risk": "medium",
                "reason": "Fake provider",
                "recommendation": "Check Odoo 19",
                "confidence": 0.95,
            }

    class FakeFactory:
        def __init__(self):
            self.called_with = []

        def create(self, config):
            self.called_with.append(config)
            return FakeProvider()

    fake_factory = FakeFactory()

    from agents.migration_agent import MigrationAgent

    agent = MigrationAgent()
    agent.provider_factory = fake_factory

    report = FakeReport()

    result = agent.create_plan(report)

    assert result["agent"] == "MigrationAgent"
    assert len(result["steps"]) == 5

    # Les findings nécessitant un LLM doivent être passés
    # par la Factory.
    assert len(fake_factory.called_with) == 5

    for config in fake_factory.called_with:
        assert config.provider == "openrouter"
        assert config.model in {
            "cheap",
            "standard",
            "powerful",
        }