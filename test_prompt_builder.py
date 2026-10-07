from agents.llm.prompt_builder import PromptBuilder


context = {
    "module": "examples/cartin_refund",
    "source_version": "16.0.1.0.0",
    "target_version": "19.0",

    "finding": {
        "type": "model",
        "severity": "info",
        "message": "Modèle Odoo détecté : cartin.refund",
    },

    "python": [
        {
            "file": "models/refund.py",
            "analysis": {
                "models": ["cartin.refund"],
                "fields": [
                    "name: Char",
                    "amount: Float",
                ],
            },
        }
    ],

    "xml": [],

    "database": {
        "database": "v16_digi",
        "status": "success",
        "tables": ["res_users", "res_partner"],
        "odoo_tables": ["res_users", "res_partner"],
        "extensions": ["pg_trgm", "plpgsql"],
    },

    "data": {
        "database": "v16_digi",
        "status": "success",
        "models": {
            "res.users": {
                "table": "res_users",
                "count": 73,
            },
            "res.partner": {
                "table": "res_partner",
                "count": 65417,
            },
        },
    },
}


builder = PromptBuilder()

prompt = builder.build(context)


print("\n===== PROMPT BUILDER TEST =====")
print(prompt)


print("\n===== VALIDATION =====")

assert "examples/cartin_refund" in prompt
print("Module : OK")

assert "16.0.1.0.0" in prompt
print("Source version : OK")

assert "19.0" in prompt
print("Target version : OK")

assert "cartin.refund" in prompt
print("Finding : OK")

assert "models/refund.py" in prompt
print("Python context : OK")

assert "CONTEXTE XML" in prompt
print("XML context : OK")

assert "CONTEXTE DATABASE" in prompt
print("Database section : OK")

assert "v16_digi" in prompt
print("Database information : OK")

assert "res_users" in prompt
print("Database tables : OK")

assert "CONTEXTE DATA" in prompt
print("Data section : OK")

assert "res.users" in prompt
print("Data model : OK")

assert "65417" in prompt
print("Data count : OK")

print("\nPromptBuilder : VALID")
