from pathlib import Path

from woop.media import prepare

image_path = Path(__file__).parent / "images" / "tell.jpg"

photo = prepare(str(image_path))

print(photo)