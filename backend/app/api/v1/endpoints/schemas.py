from fastapi import APIRouter, HTTPException
from app.services.schema_service import SchemaService

router = APIRouter()

@router.get("/schemas", response_model=list, summary="List all available form schemas")
async def list_schemas():
    """
    Returns metadata for all 13 supported form types including
    icon, description, section count, and field count.
    """
    return SchemaService.get_all()

@router.get("/schemas/{form_type}", response_model=dict, summary="Get a specific form schema")
async def get_schema(form_type: str):
    """
    Returns the full JSON schema for the requested form type.
    form_type should be URL-encoded (e.g., 'Medical Report' -> 'Medical%20Report').
    """
    schema = SchemaService.get(form_type)
    if schema is None:
        raise HTTPException(
            status_code=404,
            detail=f"Schema not found for form type: '{form_type}'"
        )
    return schema
