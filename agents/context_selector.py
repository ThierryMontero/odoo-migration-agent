class ContextSelector:

    def select(
        self,
        report,
        finding: dict,
    ) -> dict:

        data = report.to_dict()

        finding_type = finding["type"]

        context = {
            "module": data["module"],
            "source_version": (
                data["manifest"].get("version")
            ),
            "target_version": "19.0",
            "finding": finding,
            "python": [],
            "xml": [],
        }

        if finding_type == "api":

            context["python"] = (
                self._select_python_with_api(
                    data["python"]
                )
            )

        elif finding_type == "model":

            context["python"] = (
                self._select_python_with_model(
                    data["python"],
                    finding,
                )
            )

        elif finding_type == "wizard":

            context["python"] = (
                self._select_python_with_wizard(
                    data["python"]
                )
            )

        elif finding_type == "relation":

            context["python"] = (
                self._select_python_with_relation(
                    data["python"],
                    finding,
                )
            )

        else:

            context["python"] = data["python"]
            context["xml"] = data["xml"]

        return context

    # ==========================================
    # API
    # ==========================================

    def _select_python_with_api(
        self,
        python_files,
    ):

        return [
            item
            for item in python_files
            if item["analysis"].get("api_decorators")
        ]

    # ==========================================
    # MODEL
    # ==========================================

    def _select_python_with_model(
        self,
        python_files,
        finding,
    ):

        message = finding.get("message", "")

        selected = []

        for item in python_files:

            models = item["analysis"].get(
                "models",
                []
            )

            if any(
                message == f"Modèle Odoo détecté : {model}"
                for model in models
            ):
                selected.append(item)

        return selected

    # ==========================================
    # WIZARD
    # ==========================================

    def _select_python_with_wizard(
        self,
        python_files,
    ):

        return [
            item
            for item in python_files
            if "models.TransientModel"
            in item["analysis"].get(
                "model_types",
                []
            )
        ]

    # ==========================================
    # RELATION
    # ==========================================

    def _select_python_with_relation(
        self,
        python_files,
        finding,
    ):

        message = finding.get("message", "")

        selected = []

        for item in python_files:

            fields = item["analysis"].get(
                "fields",
                []
            )

            if any(
                field.split(":")[0].strip()
                in message
                for field in fields
            ):
                selected.append(item)

        return selected