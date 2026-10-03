from backend.formatters.common import sanitize_text, format_html_preview
from backend.formatters.docx_formatter import format_docx
from backend.formatters.pdf_formatter import format_pdf

SAMPLE = """DRAFT - FOR REVIEW

NON-DISCLOSURE AGREEMENT

1. Confidentiality applies to information disclosed under this agreement.
2. Information must be returned upon termination.
"""

def test_sanitize_text():
    assert sanitize_text("“Hello”—world").startswith('"Hello"-world')

def test_html_preview():
    html = format_html_preview(SAMPLE)
    assert "<h3>NON-DISCLOSURE AGREEMENT</h3>" in html
    assert "Confidentiality" in html

def test_docx_export():
    data = format_docx(SAMPLE, "NDA")
    assert data.startswith(b"PK")

def test_pdf_export():
    data = format_pdf(SAMPLE, "NDA")
    assert data.startswith(b"%PDF")
