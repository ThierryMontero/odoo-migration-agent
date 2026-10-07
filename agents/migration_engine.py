from agents.module_scanner import ModuleScanner
from agents.manifest_analyzer import ManifestAnalyzer
from agents.code_analyzer import CodeAnalyzer
from agents.migration_analyzer import MigrationAnalyzer
from agents.xml_analyzer import XMLAnalyzer
from agents.cross_analyzer import CrossAnalyzer
from agents.migration_report import MigrationReport


class MigrationEngine:

    def __init__(self):

        self.scanner = ModuleScanner()

        self.manifest_analyzer = (
            ManifestAnalyzer()
        )

        self.code_analyzer = (
            CodeAnalyzer()
        )

        self.migration_analyzer = (
            MigrationAnalyzer()
        )

        self.xml_analyzer = (
            XMLAnalyzer()
        )

        self.cross_analyzer = (
            CrossAnalyzer()
        )

    def analyze(
        self,
        module_path: str,
    ) -> MigrationReport:

        # ==========================================
        # 1. SCAN
        # ==========================================

        scan = self.scanner.scan(
            module_path
        )

        report = MigrationReport(
            module_path
        )

        # ==========================================
        # 2. MANIFEST
        # ==========================================

        if scan["manifest"]:

            manifest = (
                self.manifest_analyzer.analyze(
                    scan["manifest"]
                )
            )

            report.set_manifest(
                manifest
            )

        # ==========================================
        # 3. PYTHON
        # ==========================================

        for python_file in scan["python"]:

            if python_file.endswith(
                "__init__.py"
            ):
                continue

            with open(
                python_file,
                "r",
                encoding="utf-8",
            ) as file:

                content = file.read()

            analysis = (
                self.code_analyzer.analyze(
                    content
                )
            )

            findings = (
                self.migration_analyzer
                .analyze_python(
                    analysis
                )
            )

            report.add_python_analysis(
                python_file,
                analysis,
                findings,
            )

        # ==========================================
        # 4. XML
        # ==========================================

        for xml_file in scan["xml"]:

            analysis = (
                self.xml_analyzer.analyze(
                    xml_file
                )
            )

            report.add_xml_analysis(
                xml_file,
                analysis,
            )

        # ==========================================
        # 5. CROSS ANALYSIS
        # ==========================================

        for xml_item in report.xml:

            xml_analysis = (
                xml_item["analysis"]
            )

            for view in xml_analysis["views"]:

                matching_python = None

                for python_item in report.python:

                    python_analysis = (
                        python_item["analysis"]
                    )

                    if (
                        view["model"]
                        in python_analysis.get(
                            "models",
                            []
                        )
                    ):

                        matching_python = (
                            python_analysis
                        )

                        break

                if matching_python is None:

                    report.add_cross_findings([
                        {
                            "type": "missing_model",
                            "severity": "error",
                            "message": (
                                f"Modèle "
                                f"'{view['model']}' "
                                f"absent du Python."
                            ),
                        }
                    ])

                    continue

                findings = (
                    self.cross_analyzer
                    .compare_model_and_view(
                        matching_python,
                        view,
                    )
                )

                report.add_cross_findings(
                    findings
                )

        return report
