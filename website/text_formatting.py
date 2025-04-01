import re
from mistune import create_markdown

ALLOWED_TAGS = [
    "strong", "em", "u", "del", "code", "iframe", "br"
]

ALLOWED_ATTRIBUTES = {
    "iframe": ["src", "frameborder", "allowfullscreen","loading"],
}

def parse(text):
    markdown = create_markdown(plugins=["strikethrough"])
    return embed_youtube_links(markdown(text))

def render_discord_markup(text):
    rules = [
        (r"(\*(.*?)\*)|(_(.*?)_)", r'<span class="italic">\1</span>'),  # italic
        (r"\*\*(.*?)\*\*", r'<span class="bold">\1</span>'),  # bold
        (r"\*\*\*(.*?)\*\*\*", r'<span class="bold italic">\1</span>'), # bold italics
        (r"__(.*?)__", r'<span class="underline">\1</span>'),  # underline
        (r"__\*(.*?)\*__", r'<span class="underline italic">\1</span>'),  # underline italics
        (r"__\*\*\*(.*?)\*\*\*__", r'<span class="underline bold italic">\1</span>'),  # underline bold italics
        (r"~~(.*?)~~", r'<span class="strikethrough">\1</span>'),  # strikethrough
        (r"~~(.*?)~~", r'<span class="strikethrough">\1</span>'),  # strikethrough
        (r"`(.*?)`", r'<code>\1</code>'),  # inline code
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
        iframe = f'<iframe src="{embed_url}" frameborder="0" allowfullscreen loading="lazy"></iframe>'
        return ""

    text = re.sub(youtube_regex, replace, text)
    if iframe:
        text = f"{iframe}<br>{text}"
    return text


