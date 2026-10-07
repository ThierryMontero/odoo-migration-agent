import psycopg2

from agents.database_report import DatabaseReport


class DatabaseAgent:
    def __init__(self, config: dict):
        self.name = "DatabaseAgent"
        self.config = config

    def analyze(self) -> DatabaseReport:
        report = DatabaseReport(
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

            # Récupérer les tables
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)

            report.tables = [
                row[0]
                for row in cursor.fetchall()
            ]

            # Identifier les tables Odoo
            report.odoo_tables = [
                table
                for table in report.tables
                if table.startswith((
                    "ir_",
                    "res_",
                    "account_",
                    "stock_",
                    "product_",
                    "sale_",
                    "purchase_",
                ))
            ]

            # Récupérer les extensions PostgreSQL
            cursor.execute("""
                SELECT extname
                FROM pg_extension
                ORDER BY extname;
            """)

            report.extensions = [
                row[0]
                for row in cursor.fetchall()
            ]

            cursor.close()
            connection.close()

            report.set_success()

        except Exception as error:
            report.set_error(str(error))

        return report