import enum
from pathlib import Path
import nanoid
from PIL import Image
from . import contest_database
from .contest_database import AttachmentVariants, Attachments

class FileVariants(enum.Enum):
    THUMBNAIL = "thumbnail"
    COMPRESSED = "compressed"

def create_file_variants(session, attachment : Attachments):
    if not attachment.get_variant(FileVariants.COMPRESSED.value):
        create_compressed_variant(session, attachment)

def create_compressed_variant(session, attachment : Attachments) -> dict[FileVariants, str] | None:
    filepath = Path(attachment.filename)
    if (filepath.name.endswith(".jpg") or
            filepath.name.endswith(".jpeg") or
            filepath.name.endswith(".png") or
            filepath.name.endswith(".gif")
    ):
        webp_filename = filepath.with_suffix(".webp")
        img = Image.open(filepath)
        img.save(webp_filename, "webp", optimize=True, quality=80, method=6)

        session.add(AttachmentVariants(
            attachment_id=attachment.id,
            kind=FileVariants.COMPRESSED.value,
            filename=str(webp_filename),
        ))