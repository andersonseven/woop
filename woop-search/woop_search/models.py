from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchMatch:
    """
    Représente une occurrence trouvée
    dans un fichier.
    """

    file_path: Path

    line_number: int

    line_content: str


@dataclass
class SearchReport:
    """
    Représente le résultat complet
    d'une recherche.
    """

    query: str

    folder: Path

    matches: list[SearchMatch]

    scanned_files: int

    elapsed_time: float

    @property
    def total_matches(self) -> int:

        return len(self.matches)

    @property
    def found_files(self) -> int:

        return len(
            {
                match.file_path
                for match in self.matches
            }
        )