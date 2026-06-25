from fastapi import APIRouter
from pydantic import BaseModel
from app.classification.classifier import DocumentClassifier

router = APIRouter()

class ClassificationRequest(BaseModel):
    text: str

@router.post("/classify-document", response_model=dict, summary="Classify document type from text")
async def classify_document(request: ClassificationRequest):
    """
    Classifies the input OCR text into one of the 12 supported document types:
    Resume, Passport, Aadhaar, PAN Card, Driving License, Invoice, Bank Statement, 
    Medical Report, Research Paper, Egg AI Report, Certificate, Generic Document.
    """
    result = DocumentClassifier.classify(request.text)
    return result
