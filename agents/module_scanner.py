from pathlib import Path


class ModuleScanner:

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".xml",
        ".csv",
        ".js",
        ".scss",
        ".css",
    }

    def scan(self, module_path: str) -> dict:

        module_dir = Path(module_path)

        if not module_dir.exists():
            raise FileNotFoundError(
                f"Module introuvable : {module_path}"
            )

        if not module_dir.is_dir():
            raise ValueError(
                f"Ce chemin n'est pas un dossier : {module_path}"
            )

        result = {
            "module": str(module_dir),
            "manifest": None,
            "python": [],
            "xml": [],
            "csv": [],
            "javascript": [],
            "styles": [],
        }

        for path in sorted(module_dir.rglob("*")):

            if not path.is_file():
                continue

            if path.name == "__manifest__.py":
                result["manifest"] = str(path)
                continue

            extension = path.suffix.lower()

            if extension == ".py":
                result["python"].append(str(path))

            elif extension == ".xml":
                result["xml"].append(str(path))

            elif extension == ".csv":
                result["csv"].append(str(path))

            elif extension == ".js":
                result["javascript"].append(str(path))

            elif extension in {".scss", ".css"}:
                result["styles"].append(str(path))

        return result
