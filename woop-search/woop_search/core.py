from pathlib import Path
from time import perf_counter

from .models import SearchMatch, SearchReport


# Extensions que WOOP Search peut lire dans la v0.1
DEFAULT_EXTENSIONS = {
    ".txt",
    ".py",
    ".md",
    ".json",
    ".csv",
    ".html",
    ".css",
    ".js",
    ".xml",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
}


def search(
    folder: str | Path,
    query: str,
    *,
    recursive: bool = True,
    case_sensitive: bool = False,
    extensions: set[str] | None = None,
) -> SearchReport:
    """
    Recherche un texte dans les fichiers d'un dossier.

    Parameters
    ----------
    folder:
        Le dossier dans lequel effectuer la recherche.

    query:
        Le mot ou l'expression à rechercher.

    recursive:
        Si True, WOOP Search explore aussi les sous-dossiers.

    case_sensitive:
        Si True, la recherche distingue les majuscules
        des minuscules.

    extensions:
        Les extensions autorisées.
        Si None, les extensions par défaut sont utilisées.

    Returns
    -------
    SearchReport:
        Le rapport complet de la recherche.
    """

    # On convertit le chemin reçu en objet Path.
    folder_path = Path(folder)

    # On vérifie que le dossier existe.
    if not folder_path.exists():
        raise FileNotFoundError(
            f"Le dossier n'existe pas : {folder_path}"
        )

    # On vérifie que le chemin est bien un dossier.
    if not folder_path.is_dir():
        raise NotADirectoryError(
            f"Ce chemin n'est pas un dossier : {folder_path}"
        )

    # Une recherche vide n'a pas de sens.
    if not query:
        raise ValueError(
            "Le texte à rechercher ne peut pas être vide."
        )

    # Si l'utilisateur n'a pas donné d'extensions,
    # on utilise les extensions de WOOP Search.
    allowed_extensions = (
        DEFAULT_EXTENSIONS
        if extensions is None
        else {
            extension.lower()
            for extension in extensions
        }
    )

    # Liste qui contiendra toutes les occurrences.
    matches: list[SearchMatch] = []

    # Compteur des fichiers réellement analysés.
    scanned_files = 0

    # On démarre le chronomètre.
    start_time = perf_counter()

    # On récupère les fichiers à analyser.
    files = iter_files(
        folder=folder_path,
        recursive=recursive,
        extensions=allowed_extensions,
    )

    # On analyse chaque fichier.
    for file_path in files:

        scanned_files += 1

        file_matches = search_in_file(
            file_path=file_path,
            query=query,
            case_sensitive=case_sensitive,
        )

        matches.extend(file_matches)

    # On calcule le temps total.
    elapsed_time = perf_counter() - start_time

    # On retourne un objet SearchReport.
    return SearchReport(
        query=query,
        folder=folder_path,
        matches=matches,
        scanned_files=scanned_files,
        elapsed_time=elapsed_time,
    )


def iter_files(
    folder: Path,
    *,
    recursive: bool,
    extensions: set[str],
):
    """
    Parcourt un dossier et retourne les fichiers
    correspondant aux extensions demandées.
    """

    # rglob("*") explore le dossier et tous
    # ses sous-dossiers.
    if recursive:
        paths = folder.rglob("*")

    # glob("*") explore seulement le dossier
    # principal.
    else:
        paths = folder.glob("*")

    for path in paths:

        # On ignore les dossiers.
        if not path.is_file():
            continue

        # On récupère l'extension du fichier.
        extension = path.suffix.lower()

        # On ignore les extensions non autorisées.
        if extension not in extensions:
            continue

        yield path


def search_in_file(
    file_path: Path,
    query: str,
    *,
    case_sensitive: bool,
) -> list[SearchMatch]:
    """
    Recherche un texte dans un seul fichier.
    """

    matches: list[SearchMatch] = []

    # Pour une recherche insensible à la casse,
    # on convertit la requête en minuscules.
    search_query = (
        query
        if case_sensitive
        else query.lower()
    )

    try:

        # errors="replace" évite que le programme
        # s'arrête sur certains caractères invalides.
        with file_path.open(
            mode="r",
            encoding="utf-8",
            errors="replace",
        ) as file:

            # enumerate commence ici à 1,
            # car les lignes sont numérotées à partir de 1.
            for line_number, line in enumerate(
                file,
                start=1,
            ):

                # On enlève le retour à la ligne.
                clean_line = line.rstrip()

                # On prépare la ligne pour la comparaison.
                comparable_line = (
                    clean_line
                    if case_sensitive
                    else clean_line.lower()
                )

                # On vérifie si la recherche est présente.
                if search_query in comparable_line:

                    matches.append(
                        SearchMatch(
                            file_path=file_path,
                            line_number=line_number,
                            line_content=clean_line,
                        )
                    )

    except (OSError, UnicodeError):

        # Si un fichier est inaccessible ou illisible,
        # on l'ignore dans la v0.1.
        pass

    return matches