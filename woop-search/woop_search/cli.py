from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from .core import search
from .models import SearchReport


# Console principale de WOOP.
console = Console()


def create_parser() -> argparse.ArgumentParser:
    """
    Crée et configure les arguments
    de la commande woop-search.
    """

    parser = argparse.ArgumentParser(
        prog="woop-search",
        description=(
            "Recherche rapidement un texte "
            "dans les fichiers d'un dossier."
        ),
    )

    parser.add_argument(
        "folder",
        help="Dossier dans lequel effectuer la recherche.",
    )

    parser.add_argument(
        "query",
        help="Mot ou expression à rechercher.",
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help=(
            "Recherche uniquement dans le dossier "
            "principal, sans parcourir les sous-dossiers."
        ),
    )

    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help=(
            "Distingue les majuscules "
            "des minuscules."
        ),
    )

    return parser


def print_banner() -> None:
    """
    Affiche la bannière officielle
    de WOOP Search.
    """

    title = Text(
        "WOOP SEARCH",
        style="bold bright_cyan",
        justify="center",
    )

    subtitle = Text(
        "Small tools. Less work.",
        style="italic bright_white",
        justify="center",
    )

    content = Text.assemble(
        title,
        "\n",
        subtitle,
    )

    console.print()

    console.print(
        Panel(
            content,
            border_style="bright_cyan",
            padding=(1, 6),
        )
    )

    console.print()


def print_search_information(
    folder: str,
    query: str,
    recursive: bool,
    case_sensitive: bool,
) -> None:
    """
    Affiche les paramètres
    de la recherche.
    """

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1),
    )

    table.add_column(
        style="bold cyan",
        justify="right",
    )

    table.add_column(
        style="white",
    )

    table.add_row(
        "Recherche :",
        f"[bold yellow]{query}[/bold yellow]",
    )

    table.add_row(
        "Dossier :",
        str(Path(folder).resolve()),
    )

    table.add_row(
        "Sous-dossiers :",
        "Oui" if recursive else "Non",
    )

    table.add_row(
        "Majuscules :",
        (
            "Respectées"
            if case_sensitive
            else "Ignorées"
        ),
    )

    console.print(table)
    console.print()


def print_results(
    report: SearchReport,
) -> None:
    """
    Affiche les occurrences trouvées.
    """

    if not report.matches:

        console.print(
            Panel(
                "[bold yellow]"
                "Aucune occurrence trouvée."
                "[/bold yellow]",
                title="[bold]Résultat[/bold]",
                border_style="yellow",
            )
        )

        return

    console.print(
        Rule(
            "[bold bright_cyan]"
            "RÉSULTATS"
            "[/bold bright_cyan]"
        )
    )

    console.print()

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        expand=True,
    )

    table.add_column(
        "Fichier",
        style="bold white",
        min_width=20,
    )

    table.add_column(
        "Ligne",
        justify="center",
        style="yellow",
        width=8,
    )

    table.add_column(
        "Contenu",
        style="white",
    )

    for match in report.matches:

        try:

            relative_path = (
                match.file_path.relative_to(
                    report.folder
                )
            )

        except ValueError:

            relative_path = match.file_path

        table.add_row(
            str(relative_path),
            str(match.line_number),
            match.line_content,
        )

    console.print(table)


def print_summary(
    report: SearchReport,
) -> None:
    """
    Affiche le résumé final
    de la recherche.
    """

    console.print()

    console.print(
        Rule(
            "[bold bright_cyan]"
            "RÉSUMÉ"
            "[/bold bright_cyan]"
        )
    )

    console.print()

    summary = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
    )

    summary.add_column(
        style="bold cyan",
        justify="right",
    )

    summary.add_column(
        style="bold white",
    )

    summary.add_row(
        "Fichiers analysés :",
        str(report.scanned_files),
    )

    summary.add_row(
        "Fichiers trouvés :",
        str(report.found_files),
    )

    summary.add_row(
        "Occurrences :",
        str(report.total_matches),
    )

    summary.add_row(
        "Temps :",
        f"{report.elapsed_time:.3f} seconde(s)",
    )

    console.print(summary)

    console.print()

    console.print(
        "[dim]WOOP — Small tools. Less work.[/dim]",
        justify="center",
    )


def main() -> None:
    """
    Point d'entrée principal
    de la commande woop-search.
    """

    parser = create_parser()

    args = parser.parse_args()

    recursive = not args.no_recursive

    print_banner()

    print_search_information(
        folder=args.folder,
        query=args.query,
        recursive=recursive,
        case_sensitive=args.case_sensitive,
    )

    try:

        with console.status(
            "[bold bright_cyan]"
            "WOOP Search analyse les fichiers..."
            "[/bold bright_cyan]",
            spinner="dots",
        ):

            report = search(
                folder=args.folder,
                query=args.query,
                recursive=recursive,
                case_sensitive=(
                    args.case_sensitive
                ),
            )

    except FileNotFoundError as error:

        console.print(
            f"[bold red]Erreur :[/bold red] {error}"
        )

        sys.exit(1)

    except NotADirectoryError as error:

        console.print(
            f"[bold red]Erreur :[/bold red] {error}"
        )

        sys.exit(1)

    except ValueError as error:

        console.print(
            f"[bold red]Erreur :[/bold red] {error}"
        )

        sys.exit(1)

    print_results(report)

    print_summary(report)


if __name__ == "__main__":
    main()