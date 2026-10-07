from agents.migration_report import MigrationReport


report = MigrationReport(
    "examples/cartin_refund"
)


report.set_manifest({
    "name": "Cartin Refund",
    "version": "16.0.1.0.0",
})


report.add_python_analysis(
    "models/refund.py",
    {
        "models": ["cartin.refund"],
        "fields": [
            "name: Char",
            "amount: Float",
        ],
    },
    [
        {
            "type": "model",
            "severity": "info",
            "message": "Modèle détecté",
        }
    ],
)


print("\n===== MIGRATION REPORT =====")

print(
    report.to_dict()
)
