class DatabaseReport:
    def __init__(self, database: str):
        self.database = database
        self.status = "unknown"
        self.tables = []
        self.odoo_tables = []
        self.extensions = []
        self.error = None

    def set_success(self):
        self.status = "success"

    def set_error(self, error: str):
        self.status = "error"
        self.error = error

    def to_dict(self) -> dict:
        return {
            "database": self.database,
            "status": self.status,
            "tables": self.tables,
            "odoo_tables": self.odoo_tables,
            "extensions": self.extensions,
            "error": self.error,
        }
