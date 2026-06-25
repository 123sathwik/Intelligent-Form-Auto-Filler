from fastapi import APIRouter
from pydantic import BaseModel
from app.nlp.entity_service import EntityService

router = APIRouter()

class ExtractEntitiesRequest(BaseModel):
    text: str

@router.post("/extract-entities", response_model=dict, summary="Extract structured entities from document text")
async def extract_entities(request: ExtractEntitiesRequest):
    """
    Analyzes raw or cleaned document text using spaCy NER, regular expressions, and custom
    heuristic rules to extract structured metadata (names, contact details, education,
    skills, credentials, and government IDs).
    """
    return await EntityService.extract_entities_from_text(request.text)
