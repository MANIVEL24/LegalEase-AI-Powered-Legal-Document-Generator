from __future__ import annotations

from backend.config import settings

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover
    genai = None
    types = None

class GeminiDocumentGenerator:
    """Generate legal-document drafts with Gemini, or deterministic demo text."""

    def __init__(self) -> None:
        self.model_name = settings.gemini_model
        self.demo_mode = settings.effective_demo_mode
        self.client = None

        if not self.demo_mode:
            if genai is None:
                raise RuntimeError(
                    "The google-genai package is not installed. Run: pip install -r requirements.txt"
                )
            self.client = genai.Client(api_key=settings.gemini_api_key)

    def build_prompt(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        return f"""
You are a legal-document drafting assistant. Create a professional DRAFT legal document.

Document type: {document_type}
Parties: {parties}
Effective date: {dates}
Terms and conditions: {terms}

Requirements:
- Use clear formal legal language.
- Do not invent names, dates, monetary values, addresses, obligations, or facts.
- Use only information supplied above plus neutral drafting language.
- Organize the draft with a title, recitals/background when appropriate,
  numbered sections, and signature blocks.
- Include the supplied terms faithfully.
- If important information is missing, use a clearly marked placeholder such as [NOT PROVIDED].
- Do not claim that the document is legally valid, jurisdiction-specific, or reviewed by a lawyer.
- Return plain text only, without Markdown code fences.
- Put "DRAFT - FOR REVIEW" at the top.
"""

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        if self.demo_mode:
            return self._demo_document(document_type, parties, terms, dates)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self.build_prompt(document_type, parties, terms, dates),
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=5000,
            ),
        )
        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    @staticmethod
    def _demo_document(document_type: str, parties: str, terms: str, dates: str) -> str:
        term_items = [item.strip() for item in terms.replace("\n", ";").split(";") if item.strip()]
        lines = [
            "DRAFT - FOR REVIEW",
            "",
            document_type.upper(),
            "",
            f"Effective Date: {dates}",
            "",
            "PARTIES",
            parties,
            "",
            "AGREEMENT",
            f"This draft {document_type} is entered into by the parties identified above "
            "as of the stated effective date.",
            "",
            "TERMS AND CONDITIONS",
        ]
        for index, item in enumerate(term_items, 1):
            lines.append(f"{index}. {item}")
        lines += [
            "",
            "GENERAL",
            "The parties should review this draft and complete any missing information "
            "before signing. Jurisdiction-specific provisions may be required.",
            "",
            "SIGNATURES",
            "",
            "Party 1: ______________________________    Date: ______________",
            "Party 2: ______________________________    Date: ______________",
        ]
        return "\n".join(lines)
