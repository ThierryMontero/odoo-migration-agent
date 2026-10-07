from agents.orchestrator import Orchestrator


orchestrator = Orchestrator()

result = orchestrator.run(
    "examples/cartin_refund"
)

print("\n===== ORCHESTRATOR TEST =====")

print(
    f"Module : "
    f"{result['module']}"
)

print(
    f"Status : "
    f"{result['status']}"
)

print(
    f"Code findings : "
    f"{len(result['code_analysis']['migration_findings'])}"
)

migration_plan = result["migration_plan"]

print(
    f"Migration agent : "
    f"{migration_plan['agent']}"
)

print(
    f"Number of steps : "
    f"{len(migration_plan['steps'])}"
)

print(
    f"Global validation : "
    f"{result['global_validation']['valid']}"
)

print(
    f"Global validation errors : "
    f"{result['global_validation']['errors']}"
)

database = result["database_analysis"]

print("\n===== DATABASE ANALYSIS =====")
print(f"Status : {database['status']}")
print(f"Database : {database['database']}")
print(f"Tables : {len(database['tables'])}")
print(f"Tables Odoo : {len(database['odoo_tables'])}")
print(f"Extensions : {database['extensions']}")

data = result["data_analysis"]

print("\n===== DATA ANALYSIS =====")
print(f"Status : {data['status']}")
print(f"Database : {data['database']}")

for model, info in data["models"].items():
    print(
        f"{model} -> "
        f"table={info['table']}, "
        f"records={info['count']}"
    )

for index, step in enumerate(
    migration_plan["steps"],
    start=1,
):

    decision = (
        step["llm_result"]["decision"]
        if step["llm_result"]
        else "N/A"
    )

    print(
        f"{index}. "
        f"{step['category']} "
        f"-> "
        f"{decision}"
    )