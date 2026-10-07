from agents.llm.prompt_builder import PromptBuilder


context = {
    "module": "cartin_refund",
    "source_version": "16.0",
    "target_version": "19.0",

    "finding": {
        "type": "api",
        "severity": "warning",
        "message": (
            "Décorateur API détecté : "
            "@api.model. Vérifier son comportement "
            "en Odoo 19."
        ),
    },

    "python": [
        {
            "file": "models/refund.py",
            "analysis": {
                "models": ["cartin.refund"],
                "api_decorators": ["model"],
            },
        }
    ],

    "xml": [],
}


builder = PromptBuilder()

prompt = builder.build(context)

print(prompt)
