import re
import bleach
from markupsafe import Markup

ALLOWED_TAGS = [
    "strong", "em", "u", "del", "code", "iframe", "br"
]

ALLOWED_ATTRIBUTES = {
    "iframe": ["src", "frameborder", "allowfullscreen"],
}

def parse(text):
    text = parse_discord_markup(text)
    text = embed_youtube_links(text)
    return sanitize_html(text)

def sanitize_html(text):
    cleaned = bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return Markup(cleaned)

def parse_discord_markup(text):
    rules = [
        (r"__(.*?)__", r"<u>\1</u>"),  # underline
        (r"\*\*(.*?)\*\*", r"<strong>\1</strong>"),  # bold
        (r"\*(.*?)\*", r"<em>\1</em>"),  # italic
        (r"~~(.*?)~~", r"<del>\1</del>"),  # strikethrough
        (r"`(.*?)`", r"<code>\1</code>"),  # inline code
    ]

    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)

    return text


def embed_youtube_links(text):
    # Match common YouTube video formats and capture clean ID
    youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|shorts\/|playlist\?|watch\?v=|watch\?.+?[&;]v=))([a-zA-Z0-9\-_]{11})(?:\S+)?'
    iframe = None
    def replace(match):
        video_id = match.group(1)
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        nonlocal iframe
        iframe = f'<iframe src="{embed_url}" frameborder="0" allowfullscreen></iframe>'
        return ""

    text = re.sub(youtube_regex, replace, text)
    if iframe:
        text = f"{iframe}<br>{text}"
    return text


