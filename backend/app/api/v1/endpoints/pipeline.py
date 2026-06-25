import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.ocr.ocr_service import OCRService
from app.preprocessing.cleaning_service import CleaningService
from app.nlp.entity_service import EntityService
from app.services.schema_service import SchemaService

logger = logging.getLogger("autofiller-backend")

router = APIRouter()

class ProcessRequest(BaseModel):
    filename: str
    form_type: str
    custom_schema: Optional[dict] = None  # Only used when form_type == "Custom Form"

@router.post("/process", response_model=dict, summary="Full OCR → NLP → Autofill pipeline")
async def process_document(request: ProcessRequest):
    """
    Orchestrates the complete document processing pipeline:
    1. OCR text extraction
    2. Text cleaning / normalization
    3. NLP entity extraction
    4. Schema-based field auto-fill

    Returns the schema definition, autofill map, and pre-filled form data.
    """
    logger.info(f"Processing document: {request.filename} for form: {request.form_type}")

    # Step 1: Load schema
    if request.form_type == "Custom Form" and request.custom_schema:
        schema = SchemaService.get_custom(request.custom_schema)
    else:
        schema = SchemaService.get(request.form_type)
        if schema is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown form type: '{request.form_type}'"
            )

    # Step 2: OCR Extraction
    try:
        ocr_result = await OCRService.extract_text(request.filename)
        raw_text = ocr_result.get("text", "")
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")

    if not raw_text or not raw_text.strip():
        # Return empty form without error — document may be blank
        logger.warning("OCR returned empty text. Returning empty form.")
        autofill_map = SchemaService.autofill(schema, {})
        form_data = SchemaService.build_form_data(schema, autofill_map)
        return {
            "success": True,
            "form_type": request.form_type,
            "schema": schema,
            "raw_text": "",
            "cleaned_text": "",
            "entities": {},
            "autofill_map": autofill_map,
            "form_data": form_data,
        }

    # Step 3: Text Cleaning
    try:
        cleaned_text = CleaningService.clean_text(raw_text)
    except Exception as e:
        logger.warning(f"Text cleaning failed, using raw text: {e}")
        cleaned_text = raw_text

    # Step 4: NLP Entity Extraction
    try:
        nlp_result = await EntityService.extract_entities_from_text(cleaned_text)
        entities = nlp_result.get("entities", {})
    except Exception as e:
        logger.error(f"NLP extraction failed: {e}")
        entities = {}

    # Step 5: Schema-based autofill
    autofill_map = SchemaService.autofill(schema, entities)

    # Step 6: Build nested form data
    form_data = SchemaService.build_form_data(schema, autofill_map)

    auto_filled_count = sum(
        1 for v in autofill_map.values() if v.get("source") == "auto"
    )
    total_fields = len(autofill_map)

    logger.info(
        f"Pipeline complete. Auto-filled {auto_filled_count}/{total_fields} fields."
    )

    return {
        "success": True,
        "form_type": request.form_type,
        "schema": schema,
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "entities": entities,
        "autofill_map": autofill_map,
        "form_data": form_data,
        "stats": {
            "auto_filled": auto_filled_count,
            "empty": total_fields - auto_filled_count,
            "total": total_fields,
        }
    }
