from dataclasses import dataclass


@dataclass
class PreparedMedia:
    """
    Represents an image prepared by WOOP.
    """

    filename: str
    extension: str
    path: str
    width: int
    height: int
    size: int
    mime_type: str