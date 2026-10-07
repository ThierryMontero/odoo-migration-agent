from agents.orchestrator import Orchestrator


orchestrator = Orchestrator()

result = orchestrator.run(
    "examples/cartin_refund"
)

migration_plan = result["migration_plan"]


print("\n===== MIGRATION PLAN =====")

print(
    f"\nAgent : "
    f"{migration_plan['agent']}"
)

print(
    f"Module : "
    f"{migration_plan['module']}"
)

for index, step in enumerate(
    migration_plan["steps"],
    start=1,
):

    llm_status = (
        "LLM"
        if step["requires_llm"]
        else "CODE"
    )

    print(
        f"\n{index}. "
        f"[P{step['priority']}] "
        f"[{llm_status}] "
        f"{step['category']}"
    )

    print(
        f"   Action : "
        f"{step['action']}"
    )

    print(
        f"   Finding : "
        f"{step['finding']}"
    )

    if step["llm_result"]:

        result = step["llm_result"]

        print(
            f"   Decision : "
            f"{result['decision']}"
        )

        print(
            f"   Risk : "
            f"{result['risk']}"
        )

        print(
            f"   Reason : "
            f"{result['reason']}"
        )

        print(
            f"   Recommendation : "
            f"{result['recommendation']}"
        )

        print(
            f"   Confidence : "
            f"{result['confidence']}"
        )

        validation = step["validation"]

        print(
            f"   Validation : "
            f"{validation['valid']}"
        )

        if not validation["valid"]:
            print(
                f"   Validation errors : "
                f"{validation['errors']}"
            )