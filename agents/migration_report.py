class MigrationReport:

    def __init__(self, module_path: str):

        self.module = module_path

        self.manifest = {}

        self.python = []

        self.xml = []

        self.migration_findings = []

        self.cross_findings = []

    def add_python_analysis(
        self,
        file_path: str,
        analysis: dict,
        findings: list,
    ):

        self.python.append({
            "file": file_path,
            "analysis": analysis,
            "findings": findings,
        })

        self.migration_findings.extend(
            findings
        )

    def add_xml_analysis(
        self,
        file_path: str,
        analysis: dict,
    ):

        self.xml.append({
            "file": file_path,
            "analysis": analysis,
        })

    def add_cross_findings(
        self,
        findings: list,
    ):

        self.cross_findings.extend(
            findings
        )

    def set_manifest(
        self,
        manifest: dict,
    ):

        self.manifest = manifest

    def to_dict(self) -> dict:

        return {
            "module": self.module,
            "manifest": self.manifest,
            "python": self.python,
            "xml": self.xml,
            "migration_findings": (
                self.migration_findings
            ),
            "cross_findings": (
                self.cross_findings
            ),
        }
