from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.services.document_service import DocumentService
from app.ocr.ocr_service import OCRService

router = APIRouter()

class ExtractionRequest(BaseModel):
    filename: str

@router.post("/upload", response_model=dict, summary="Upload a document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, DOCX, JPG, JPEG, PNG) up to 20MB.
    Generates a unique UUID filename and saves the file locally.
    """
    return await DocumentService.save_uploaded_file(file)

@router.post("/extract-text", response_model=dict, summary="Extract text from an uploaded document")
async def extract_text(request: ExtractionRequest):
    """
    Extracts text from an uploaded document (PDF, DOCX, JPG, JPEG, PNG)
    using OCR, PyMuPDF, or python-docx. Returns cleaned text.
    """
    return await OCRService.extract_text(request.filename)

