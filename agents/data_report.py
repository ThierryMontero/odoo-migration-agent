class DataReport:
    def __init__(self, database: str):
        self.database = database
        self.status = "unknown"
        self.models = {}
        self.error = None

    def set_success(self):
        self.status = "success"

    def set_error(self, error: str):
        self.status = "error"
        self.error = error

    def add_model(self, model: str, table: str, count: int):
        self.models[model] = {
            "table": table,
            "count": count,
        }

    def to_dict(self) -> dict:
        return {
            "database": self.database,
            "status": self.status,
            "models": self.models,
            "error": self.error,
        }
