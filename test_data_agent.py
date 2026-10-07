from agents.data_agent import DataAgent


config = {
    "host": "localhost",
    "port": 5432,
    "database": "v16_digi",
    "user": "postgres",
    "password": "postgres",
}

agent = DataAgent(config)

report = agent.analyze()

print("\n===== DATA AGENT TEST =====")
print(f"Database : {report.database}")
print(f"Status : {report.status}")

if report.status == "success":
    for model, data in report.models.items():
        print(
            f"{model} -> "
            f"table={data['table']}, "
            f"records={data['count']}"
        )
else:
    print(f"Error : {report.error}")

print("\n===== DATA REPORT =====")
print(report.to_dict())
