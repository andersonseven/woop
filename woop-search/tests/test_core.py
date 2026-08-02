from pathlib import Path

import pytest

from woop_search.core import search


def test_search_finds_text(
    tmp_path: Path,
):
    """
    Vérifie que WOOP Search
    trouve un texte présent.
    """

    file = tmp_path / "example.txt"

    file.write_text(
        "Bonjour\n"
        "TODO : ajouter les tests\n"
        "Au revoir",
        encoding="utf-8",
    )

    report = search(
        folder=tmp_path,
        query="TODO",
    )

    assert report.total_matches == 1

    assert report.found_files == 1

    assert (
        report.matches[0].line_number == 2
    )

    assert (
        report.matches[0].line_content
        == "TODO : ajouter les tests"
    )


def test_search_is_case_insensitive(
    tmp_path: Path,
):
    """
    Vérifie que la recherche ignore
    les majuscules par défaut.
    """

    file = tmp_path / "example.txt"

    file.write_text(
        "TODO : terminer WOOP Search",
        encoding="utf-8",
    )

    report = search(
        folder=tmp_path,
        query="todo",
    )

    assert report.total_matches == 1


def test_case_sensitive_search(
    tmp_path: Path,
):
    """
    Vérifie que la recherche respecte
    les majuscules si demandée.
    """

    file = tmp_path / "example.txt"

    file.write_text(
        "TODO : terminer WOOP Search",
        encoding="utf-8",
    )

    report = search(
        folder=tmp_path,
        query="todo",
        case_sensitive=True,
    )

    assert report.total_matches == 0


def test_search_in_subdirectories(
    tmp_path: Path,
):
    """
    Vérifie que les sous-dossiers
    sont parcourus par défaut.
    """

    subfolder = tmp_path / "src"

    subfolder.mkdir()

    file = subfolder / "main.py"

    file.write_text(
        "# TODO : écrire le code",
        encoding="utf-8",
    )

    report = search(
        folder=tmp_path,
        query="TODO",
    )

    assert report.total_matches == 1

    assert report.found_files == 1


def test_no_recursive_search(
    tmp_path: Path,
):
    """
    Vérifie que les sous-dossiers
    sont ignorés avec recursive=False.
    """

    subfolder = tmp_path / "src"

    subfolder.mkdir()

    file = subfolder / "main.py"

    file.write_text(
        "# TODO : écrire le code",
        encoding="utf-8",
    )

    report = search(
        folder=tmp_path,
        query="TODO",
        recursive=False,
    )

    assert report.total_matches == 0


def test_missing_folder_raises_error(
    tmp_path: Path,
):
    """
    Vérifie qu'une erreur est levée
    si le dossier n'existe pas.
    """

    missing_folder = (
        tmp_path / "dossier_inexistant"
    )

    with pytest.raises(
        FileNotFoundError
    ):

        search(
            folder=missing_folder,
            query="TODO",
        )