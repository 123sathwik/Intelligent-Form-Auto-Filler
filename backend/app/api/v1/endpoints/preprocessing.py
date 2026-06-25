from fastapi import APIRouter
from pydantic import BaseModel
from app.preprocessing.cleaning_service import CleaningService

router = APIRouter()

class CleanTextRequest(BaseModel):
    text: str

@router.post("/clean-text", response_model=dict, summary="Clean and normalize OCR output")
async def clean_ocr_text(request: CleanTextRequest):
    """
    Cleans raw OCR output text by normalizing Unicode characters, reducing spacing,
    removing duplicate/blank lines, removing artifacts, and parsing standard structures
    like emails, phone numbers, and dates.
    """
    cleaned = CleaningService.clean_text(request.text)
    return {
        "success": True,
        "original_text": request.text,
        "cleaned_text": cleaned
    }
