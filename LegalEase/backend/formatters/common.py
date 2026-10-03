from html import escape
import re

def sanitize_text(text: str) -> str:
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\S\r\n]+", " ", text)
    return text.strip()

def format_html_preview(text: str) -> str:
    safe = escape(sanitize_text(text))
    paragraphs = safe.split("\n")
    body = []
    for line in paragraphs:
        stripped = line.strip()
        if not stripped:
            body.append("<div class='spacer'></div>")
        elif re.match(r"^\d+\.\s+", stripped):
            body.append(f"<p class='term'>{stripped}</p>")
        elif stripped.isupper() and len(stripped) < 100:
            body.append(f"<h3>{stripped}</h3>")
        else:
            body.append(f"<p>{stripped}</p>")
    return "\n".join(body)
