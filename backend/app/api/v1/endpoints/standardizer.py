from fastapi import APIRouter
from app.standardizer.standardizer import Standardizer

router = APIRouter()

@router.post("/standardize", response_model=dict, summary="Standardize extracted document entities")
async def standardize_entities(request: dict):
    """
    Accepts raw or variable extracted entities JSON and maps/normalizes them 
    into the correct standard intermediate JSON schema based on the document type.
    """
    entities = request.get("entities", request)
    document_type = request.get("document_type", "Generic Document")
    return Standardizer.standardize(entities, document_type)
