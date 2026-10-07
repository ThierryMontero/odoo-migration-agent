from agents.context_selector import ContextSelector


class MigrationContext:

    def __init__(self):
        self.selector = ContextSelector()

    def build(
        self,
        report,
        finding: dict,
        database_report=None,
        data_report=None,
    ) -> dict:

        context = self.selector.select(
            report,
            finding,
        )

        if database_report is not None:
            context["database"] = database_report.to_dict()

        if data_report is not None:
            context["data"] = data_report.to_dict()

        return context