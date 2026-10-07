from agents.migration_engine import MigrationEngine


class CodeAgent:

    def __init__(self):

        self.name = "CodeAgent"

        self.engine = MigrationEngine()

    def analyze_module(
        self,
        module_path: str,
    ):

        print(
            f"[{self.name}] "
            f"Analyse du module : "
            f"{module_path}"
        )

        report = self.engine.analyze(
            module_path
        )

        return report