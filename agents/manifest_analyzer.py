import ast


class ManifestAnalyzer:

    def analyze(self, manifest_path: str) -> dict:
        """
        Analyse le fichier __manifest__.py
        sans exécuter son code.
        """

        with open(
            manifest_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

        data = ast.literal_eval(content)

        return {
            "name": data.get("name"),
            "version": data.get("version"),
            "depends": data.get("depends", []),
            "data": data.get("data", []),
            "demo": data.get("demo", []),
            "assets": data.get("assets", {}),
            "installable": data.get("installable", True),
            "application": data.get("application", False),
        }