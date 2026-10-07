class MigrationPlanner:

    def create_plan(self, module_path: str, files: list[str]) -> list[dict]:
        """
        Crée un plan d'analyse pour un module Odoo.
        """

        plan = []

        for file_path in files:

            if file_path.endswith(".py"):

                plan.append({
                    "action": "read_file",
                    "target": file_path,
                    "reason": "Analyser le code Python Odoo",
                })

        return plan
