import pathlib

from PIL import Image

SUB = pathlib.Path("contests/submissions")

types = [
    SUB.rglob("*.jpg"),
    SUB.rglob("*.png"),
    SUB.rglob("*.jpeg"),
    
]

for typ in types:
    for file in typ:
        file: pathlib.Path = file.resolve()

        webp = file.with_suffix(".webp")
        if webp.is_file():
            continue

        print(f"Processing file {file}")
        img = Image.open(str(file))
        img.save(webp, "webp", optimize=True, quality=100, method=6)
