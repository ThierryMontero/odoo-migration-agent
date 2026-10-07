from agents.database_agent import DatabaseAgent


config = {
    "host": "localhost",
    "port": 5999,
    "database": "v16_digi",
    "user": "postgres",
    "password": "postgres",
}

agent = DatabaseAgent(config)

report = agent.analyze()

print("\n===== DATABASE AGENT TEST =====")
print(f"Database : {report.database}")
print(f"Status : {report.status}")

if report.status == "success":
    print(f"Tables : {len(report.tables)}")
    print(f"Tables Odoo : {len(report.odoo_tables)}")
    print(f"Extensions : {report.extensions}")
else:
    print(f"Error : {report.error}")

print("\n===== DATABASE REPORT =====")
print(report.to_dict())