import html
from datetime import date
import requests
import streamlit as st

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

BACKEND_URL = st.sidebar.text_input(
    "Backend URL",
    value="http://127.0.0.1:8000",
    help="URL of the FastAPI server.",
).rstrip("/")

st.markdown("""
<style>
.legal-card {
    background:#111827;
    color:#f9fafb;
    border:1px solid #374151;
    border-radius:14px;
    padding:24px;
    max-height:600px;
    overflow-y:auto;
    line-height:1.65;
}
.legal-card h3 { color:#93c5fd; margin-top:18px; }
.legal-card .term { margin-left:12px; }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ LegalEase")
st.caption("AI-powered legal document drafting workspace")
st.warning(
    "LegalEase creates drafts for review. It is not a substitute for advice from a qualified lawyer."
)

with st.form("document_form"):
    col1, col2 = st.columns(2)
    with col1:
        document_type = st.text_input(
            "Document Type",
            value="Freelance Work Contract",
            placeholder="e.g. NDA, Lease Agreement, Employment Contract",
        )
        parties = st.text_area(
            "Parties Involved",
            value="Jane Doe (Service Provider), TechNova Inc. (Client)",
            height=120,
        )
    with col2:
        effective_date = st.date_input("Effective Date", value=date.today())
        terms = st.text_area(
            "Terms & Conditions",
            value=(
                "Payment to be made within 30 days of invoice; "
                "The provider agrees to deliver work by the agreed deadline; "
                "Confidentiality must be maintained at all times; "
                "Either party may terminate with 15 days notice"
            ),
            height=120,
            help="Separate individual terms with semicolons.",
        )
    submitted = st.form_submit_button("Generate Document", type="primary", use_container_width=True)

if submitted:
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": effective_date.strftime("%B %d, %Y"),
    }
    try:
        with st.spinner("Generating your draft..."):
            response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        st.session_state["document"] = result["document"]
        st.session_state["document_type"] = document_type
        st.session_state["demo_mode"] = result.get("demo_mode", False)
        st.success("Document generated.")
    except requests.RequestException as exc:
        st.error(f"Could not reach the FastAPI backend: {exc}")

document = st.session_state.get("document", "")
if document:
    if st.session_state.get("demo_mode"):
        st.info("Demo mode is active. Add GEMINI_API_KEY to .env and restart the backend for Gemini generation.")

    st.subheader("Document Preview")

    edit = st.checkbox("Edit Document")
    if edit:
        document = st.text_area(
            "Editable document",
            value=document,
            height=500,
            key="editable_document",
        )
        st.session_state["document"] = document

    from backend.formatters.common import format_html_preview
    st.markdown(
        f"<div class='legal-card'>{format_html_preview(document)}</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Download")
    doc_type = st.session_state.get("document_type", "Legal Document")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Download TXT",
            data=document.encode("utf-8"),
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    from backend.formatters.docx_formatter import format_docx
    from backend.formatters.pdf_formatter import format_pdf

    docx_bytes = format_docx(document, doc_type)
    pdf_bytes = format_pdf(document, doc_type)

    with c2:
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name="legalease_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption("LegalEase • Review AI-generated drafts before signing or relying on them.")
