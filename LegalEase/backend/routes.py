from fastapi import APIRouter, HTTPException
from backend.schemas import DocumentRequest, DocumentResponse
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

@router.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "demo_mode": generator.demo_mode}

@router.post("/generate", response_model=DocumentResponse, tags=["Documents"])
def generate_document(request: DocumentRequest):
    try:
        text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return DocumentResponse(
            document=text,
            model=generator.model_name,
            demo_mode=generator.demo_mode,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Document generation failed: {exc}") from exc
