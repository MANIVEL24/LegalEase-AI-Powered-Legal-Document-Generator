from io import BytesIO
from pathlib import Path
import re

from fpdf import FPDF

from backend.formatters.common import sanitize_text

BASE_DIR = Path(__file__).resolve().parents[2]
LOGO = BASE_DIR / "assets" / "logo.png"

class LegalEasePDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type

    def header(self):
        if LOGO.exists():
            try:
                self.image(str(LOGO), x=95, y=8, w=20)
                self.set_y(31)
            except Exception:
                self.set_y(10)
        else:
            self.set_y(10)
        self.set_font("Times", "B", 12)
        self.cell(0, 8, self.doc_type.upper(), ln=True, align="C")
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "", 8)
        self.cell(0, 8, "LegalEase - AI-generated draft. Review before use.", align="C")

def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalEasePDF(doc_type)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Times", "", 11)

    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line:
            pdf.ln(3)
            continue
        if line.startswith("DRAFT"):
            pdf.set_font("Times", "B", 11)
            pdf.multi_cell(0, 6, line)
            pdf.set_font("Times", "", 11)
        elif line.isupper() and len(line) < 100:
            pdf.set_font("Times", "B", 11)
            pdf.multi_cell(0, 6, line)
            pdf.set_font("Times", "", 11)
        else:
            pdf.multi_cell(0, 6, line)
        pdf.ln(1)

    data = pdf.output()
    return bytes(data)
