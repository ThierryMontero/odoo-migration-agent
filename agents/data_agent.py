import psycopg2

from agents.data_report import DataReport


class DataAgent:
    def __init__(self, config: dict):
        self.name = "DataAgent"
        self.config = config

    def analyze(self) -> DataReport:
        report = DataReport(
            database=self.config["database"]
        )

        try:
            connection = psycopg2.connect(
                host=self.config["host"],
                port=self.config["port"],
                dbname=self.config["database"],
                user=self.config["user"],
                password=self.config["password"],
            )

            cursor = connection.cursor()

            models = {
                "res.users": "res_users",
                "res.partner": "res_partner",
                "ir.model": "ir_model",
                "ir.model.fields": "ir_model_fields",
                "ir.module.module": "ir_module_module",
            }

            for model, table in models.items():
                cursor.execute(
                    f'SELECT COUNT(*) FROM "{table}";'
                )

                count = cursor.fetchone()[0]

                report.add_model(
                    model=model,
                    table=table,
                    count=count,
                )

            cursor.close()
            connection.close()

            report.set_success()

        except Exception as error:
            report.set_error(str(error))

        return report
