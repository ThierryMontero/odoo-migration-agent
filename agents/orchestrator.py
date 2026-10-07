from agents.code_agent import CodeAgent
from agents.migration_agent import MigrationAgent
from agents.global_validation_agent import GlobalValidationAgent
from agents.database_agent import DatabaseAgent
from agents.data_agent import DataAgent

class Orchestrator:
    def __init__(self):
        self.name = "Orchestrator"
        self.code_agent = CodeAgent()
        self.migration_agent = MigrationAgent()
        self.global_validator = GlobalValidationAgent()

        self.database_agent = DatabaseAgent({
            "host": "localhost",
            "port": 5432,
            "database": "v16_digi",
            "user": "postgres",
            "password": "postgres",
        })

        self.data_agent = DataAgent({
            "host": "localhost",
            "port": 5432,
            "database": "v16_digi",
            "user": "postgres",
            "password": "postgres",
        })

    def run(self, module_path: str) -> dict:
        report = self.code_agent.analyze_module(module_path)

        database_report = self.database_agent.analyze()
        
        data_report = self.data_agent.analyze()

        migration_plan = self.migration_agent.create_plan(report)

        global_validation = self.global_validator.validate(
            migration_plan
        )

        report_data = report.to_dict()

        return {
            "module": report_data["module"],
            "status": "success",
            "code_analysis": report_data,
            "database_analysis": database_report.to_dict(),
            "data_analysis": data_report.to_dict(),
            "migration_plan": migration_plan,
            "global_validation": global_validation,
        }