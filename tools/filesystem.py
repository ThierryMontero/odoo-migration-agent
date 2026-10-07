from pathlib import Path


def read_file(path: str) -> str:
    """
    Lit un fichier texte et retourne son contenu.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Ce chemin n'est pas un fichier : {path}"
        )

    return file_path.read_text(encoding="utf-8")


def list_python_files(directory: str) -> list[str]:
    """
    Retourne les chemins des fichiers Python présents
    dans un dossier.
    """

    dir_path = Path(directory)

    if not dir_path.exists():
        raise FileNotFoundError(
            f"Dossier introuvable : {directory}"
        )

    if not dir_path.is_dir():
        raise ValueError(
            f"Ce chemin n'est pas un dossier : {directory}"
        )

    return sorted(
        str(path)
        for path in dir_path.rglob("*.py")
    )