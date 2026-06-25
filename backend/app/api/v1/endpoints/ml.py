from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.ml.field_mapper import FieldMapper

router = APIRouter()

class MapFieldsRequest(BaseModel):
    labels: List[str]

@router.post("/map-fields", response_model=dict, summary="Semantically map unknown form labels to standard fields")
async def map_fields(request: MapFieldsRequest):
    """
    Accepts a list of unknown form labels and resolves them semantically to standard keys 
    using SentenceTransformers and trained classifiers, returning mappings and confidence scores.
    """
    mappings, confidences = FieldMapper.map_labels(request.labels)
    return {
        "success": True,
        "mappings": mappings,
        "confidences": confidences
    }
