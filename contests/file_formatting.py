from PIL import Image

def format_file(filepath):
    if (filepath.name.endswith(".jpg") or
            filepath.name.endswith(".jpeg") or
            filepath.name.endswith(".png")):
        webp = filepath.with_suffix(".webp")
        img = Image.open(filepath.name)
        img.save(webp, "webp", optimize=True, quality=100, method=6)