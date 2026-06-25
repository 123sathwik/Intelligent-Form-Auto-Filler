import json
import logging
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

logger = logging.getLogger("autofiller-backend")

router = APIRouter()

# Output directory: backend/output/
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent.parent / "output"


class SubmitRequest(BaseModel):
    form_type: str
    filename: str
    form_data: Any
    autofill_map: Any = None
    stats: Any = None


@router.post("/submit", response_model=dict, summary="Submit and save a completed form")
async def submit_form(request: SubmitRequest):
    """
    Validates and saves the completed form to backend/output/ as a JSON file.
    Filename format: YYYYMMDD_HHMMSS_form.json
    """
    # Ensure output directory exists
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create output directory: {e}")

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_form_type = request.form_type.replace(" ", "_").lower()
    output_filename = f"{timestamp}_{safe_form_type}_form.json"
    output_path = OUTPUT_DIR / output_filename

    # Build output payload
    payload = {
        "metadata": {
            "form_type": request.form_type,
            "source_filename": request.filename,
            "submitted_at": datetime.now().isoformat(),
            "output_file": output_filename,
            "stats": request.stats or {}
        },
        "form_data": request.form_data,
        "autofill_map": request.autofill_map or {}
    }

    # Save to disk
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        logger.info(f"Form saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save form: {e}")
        return {"success": False, "error": str(e)}

    return {
        "success": True,
        "message": "Form submitted and saved successfully.",
        "filename": output_filename,
        "path": str(output_path),
        "submitted_at": payload["metadata"]["submitted_at"]
    }
