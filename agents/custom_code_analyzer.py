from pathlib import Path

from agents.code_analyzer import CodeAnalyzer
from agents.manifest_analyzer import ManifestAnalyzer
from agents.module_scanner import ModuleScanner
from agents.xml_analyzer import XMLAnalyzer
from agents.functional_analyzer import FunctionalAnalyzer


class CustomCodeAnalyzer:
    """
    Analyse structurée d'un module custom Odoo.

    La V1 orchestre les analyseurs déterministes existants :
    - ModuleScanner
    - ManifestAnalyzer
    - CodeAnalyzer
    - XMLAnalyzer

    Aucun LLM n'est utilisé ici.
    """

    def __init__(self):
        self.scanner = ModuleScanner()
        self.code_analyzer = CodeAnalyzer()
        self.xml_analyzer = XMLAnalyzer()
        self.manifest_analyzer = ManifestAnalyzer()
        self.functional_analyzer = FunctionalAnalyzer()

    def analyze(self, module_path: str) -> dict:

        module = Path(module_path)

        scan = self.scanner.scan(str(module))

        result = {
            "type": "custom_code",
            "module": str(module),
            "manifest": None,
            "python": [],
            "xml": [],
            "csv": scan["csv"],
            "javascript": scan["javascript"],
            "styles": scan["styles"],
        }

        # -------------------------------------------------
        # Manifest
        # -------------------------------------------------

        if scan["manifest"]:
            result["manifest"] = (
                self.manifest_analyzer.analyze(
                    scan["manifest"]
                )
            )

        # -------------------------------------------------
        # Python
        # -------------------------------------------------

        for python_file in scan["python"]:

            path = Path(python_file)

            # __manifest__.py est déjà traité séparément.
            if path.name == "__manifest__.py":
                continue

            content = path.read_text(
                encoding="utf-8"
            )

            analysis = self.code_analyzer.analyze(
                content
            )

            analysis["file"] = str(
                path.relative_to(module)
            )

            result["python"].append(
                analysis
            )

        # -------------------------------------------------
        # XML
        # -------------------------------------------------

        for xml_file in scan["xml"]:

            analysis = self.xml_analyzer.analyze(
                xml_file
            )

            analysis["file"] = str(
                Path(xml_file).relative_to(module)
            )

            result["xml"].append(
                analysis
            )

        aggregated_code_analysis = {
            "classes": [],
            "models": [],
            "inherits": [],
            "model_types": [],
            "descriptions": [],
            "fields": [],
            "api_decorators": [],
            "methods": [],
        }

        for python_analysis in result["python"]:
            for key in aggregated_code_analysis:
                aggregated_code_analysis[key].extend(
                    python_analysis.get(key, [])
                )

        functional_analysis = self.functional_analyzer.analyze(
            code_analysis=aggregated_code_analysis,
            xml_analysis={
                "views": [
                    view
                    for xml in result["xml"]
                    for view in xml.get("views", [])
                ],
                "actions": [
                    action
                    for xml in result["xml"]
                    for action in xml.get("actions", [])
                ],
                "menus": [
                    menu
                    for xml in result["xml"]
                    for menu in xml.get("menus", [])
                ],
                "records": [
                    record
                    for xml in result["xml"]
                    for record in xml.get("records", [])
                ],
                "reports": [
                    report
                    for xml in result["xml"]
                    for report in xml.get("reports", [])
                ],
            },
            manifest=result["manifest"],
        )

        result["functional"] = functional_analysis

        return result
