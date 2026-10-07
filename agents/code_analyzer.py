import ast
import re


class CodeAnalyzer:

    def analyze(self, content: str) -> dict:

        return {
            "classes": self._find_classes(content),
            "models": self._find_models(content),
            "inherits": self._find_inherits(content),
            "model_types": self._find_model_types(content),
            "descriptions": self._find_descriptions(content),
            "fields": self._find_fields(content),
            "api_decorators": self._find_api_decorators(content),
            "methods": self._find_methods(content),
            "field_metadata": self._find_field_metadata(content),
        }

    def _find_classes(self, content: str) -> list[str]:

        pattern = r"class\s+(\w+)\s*\("

        return re.findall(
            pattern,
            content,
        )

    def _find_models(self, content: str) -> list[str]:

        pattern = r"_name\s*=\s*[\"']([^\"']+)[\"']"

        return re.findall(
            pattern,
            content,
        )

    def _find_inherits(self, content: str) -> list[str]:

        pattern = r"_inherit\s*=\s*[\"']([^\"']+)[\"']"

        return re.findall(
            pattern,
            content,
        )

    def _find_model_types(self, content: str) -> list[str]:

        pattern = (
            r"class\s+\w+\s*"
            r"\(\s*(models\.(?:Model|TransientModel|AbstractModel))"
        )

        return re.findall(
            pattern,
            content,
        )

    def _find_descriptions(self, content: str) -> list[str]:

        pattern = (
            r"_description\s*=\s*[\"']([^\"']+)[\"']"
        )

        return re.findall(
            pattern,
            content,
        )

    def _find_fields(self, content: str) -> list[str]:

        pattern = (
            r"(\w+)\s*=\s*fields\.(\w+)"
        )

        matches = re.findall(
            pattern,
            content,
        )

        return [
            f"{name}: {field_type}"
            for name, field_type in matches
        ]

    def _find_api_decorators(self, content: str) -> list[str]:

        pattern = r"@api\.(\w+)"

        return re.findall(
            pattern,
            content,
        )

    def _find_methods(self, content: str) -> list[str]:

        pattern = r"^\s*def\s+(\w+)\s*\("

        return re.findall(
            pattern,
            content,
            re.MULTILINE,
        )

    def _find_field_metadata(self, content: str) -> list[dict]:
        """
        Extrait les métadonnées des déclarations fields.*.

        Exemple :

            x_total = fields.Float(
                compute="_compute_total",
                store=True,
            )

        devient :

            {
                "name": "x_total",
                "type": "Float",
                "compute": "_compute_total",
                "store": True,
                "related": None,
                "readonly": None,
            }
        """

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        metadata = []

        for node in ast.walk(tree):

            if not isinstance(node, ast.Assign):
                continue

            if len(node.targets) != 1:
                continue

            target = node.targets[0]

            if not isinstance(target, ast.Name):
                continue

            value = node.value

            if not isinstance(value, ast.Call):
                continue

            # Vérifie fields.Float, fields.Char, fields.Many2one, etc.
            if not (
                isinstance(value.func, ast.Attribute)
                and isinstance(value.func.value, ast.Name)
                and value.func.value.id == "fields"
            ):
                continue

            field_name = target.id
            field_type = value.func.attr

            kwargs = {}

            for keyword in value.keywords:
                if keyword.arg is None:
                    continue

                kwargs[keyword.arg] = self._ast_value(keyword.value)

            metadata.append({
                "name": field_name,
                "type": field_type,
                "compute": kwargs.get("compute"),
                "store": kwargs.get("store"),
                "related": kwargs.get("related"),
                "readonly": kwargs.get("readonly"),
            })

        return metadata


    @staticmethod
    def _ast_value(node):
        """
        Convertit les valeurs AST simples en valeurs Python.
        """
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError):
            return None