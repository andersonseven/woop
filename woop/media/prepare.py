from pathlib import Path

from PIL import Image

from .models import PreparedMedia


def prepare(file_path: str) -> PreparedMedia:
    """
    Read an image and return its metadata.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    with Image.open(path) as image:

        width = image.width
        height = image.height

        mime_type = Image.MIME.get(image.format, "")

    size_bytes = path.stat().st_size

    return PreparedMedia(
        filename=path.name,
        extension=path.suffix.lstrip("."),
        path=str(path),
        width=width,
        height=height,
        size=size_bytes,
        mime_type=mime_type
    )