from agents.migration_context import MigrationContext
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
            "migration_findings": [],
            "cross_findings": [],
        }


report = FakeReport()

finding = {
    "type": "model",
    "severity": "info",
    "message": "Modèle Odoo détecté : cartin.refund",
}

context_builder = MigrationContext()


# ============================================================
# TEST 1 — Ancien comportement
# ============================================================

context_v1 = context_builder.build(
    report,
    finding,
)

print("\n===== MIGRATION CONTEXT V1 =====")
print(context_v1)


# ============================================================
# TEST 2 — Nouveau comportement
# ============================================================

database_report = DatabaseReport("v16_digi")
database_report.set_success()
database_report.tables = ["res_users", "res_partner"]
database_report.odoo_tables = ["res_users", "res_partner"]
database_report.extensions = ["pg_trgm", "plpgsql"]


data_report = DataReport("v16_digi")
data_report.set_success()
data_report.add_model("res.users", "res_users", 73)
data_report.add_model("res.partner", "res_partner", 65417)


context_v2 = context_builder.build(
    report,
    finding,
    database_report=database_report,
    data_report=data_report,
)

print("\n===== MIGRATION CONTEXT V2 =====")
print(context_v2)


# ============================================================
# VERIFICATIONS
# ============================================================

print("\n===== VALIDATION =====")

assert context_v1 is not None
print("V1 : OK")

assert "database" in context_v2
assert "data" in context_v2
print("V2 : database + data présents")

assert context_v2["database"]["database"] == "v16_digi"
assert context_v2["data"]["database"] == "v16_digi"
print("Database/Data reports : OK")

print("\nMigrationContext V2 : VALID")
