from agents.migration_agent import MigrationAgent
from agents.database_report import DatabaseReport
from agents.data_report import DataReport


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
                }
            ],
            "cross_findings": [],
        }


# ============================================================
# RAPPORT CODE
# ============================================================

report = FakeReport()


# ============================================================
# RAPPORT DATABASE
# ============================================================

database_report = DatabaseReport("v16_digi")
database_report.set_success()

database_report.tables = [
    "res_users",
    "res_partner",
]

database_report.odoo_tables = [
    "res_users",
    "res_partner",
]

database_report.extensions = [
    "pg_trgm",
    "plpgsql",
]


# ============================================================
# RAPPORT DATA
# ============================================================

data_report = DataReport("v16_digi")
data_report.set_success()

data_report.add_model(
    "res.users",
    "res_users",
    73,
)

data_report.add_model(
    "res.partner",
    "res_partner",
    65417,
)


# ============================================================
# MIGRATION AGENT
# ============================================================

agent = MigrationAgent()


# ============================================================
# TEST
# ============================================================

plan = agent.create_plan(
    report,
    database_report=database_report,
    data_report=data_report,
)


# ============================================================
# AFFICHAGE
# ============================================================

print("\n===== MIGRATION AGENT CONTEXT TEST =====")
print(plan)


# ============================================================
# VALIDATIONS
# ============================================================

print("\n===== VALIDATION =====")

assert plan["agent"] == "MigrationAgent"
print("Agent : OK")

assert len(plan["steps"]) == 1
print("Nombre de findings : 1")

step = plan["steps"][0]

assert step["category"] == "model"
print("Finding : OK")

assert step["llm_result"] is not None
print("LLM result : OK")

assert step["validation"] is not None
print("Validation : OK")

print("\nMigrationAgent + MigrationContext V2 : VALID")
