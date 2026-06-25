import os
import uuid
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException

logger = logging.getLogger("autofiller-backend")

# Resolve directories relative to backend root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/png"
}

class DocumentService:
    @staticmethod
    async def save_uploaded_file(file: UploadFile) -> dict:
        filename = file.filename or ""
        ext = Path(filename).suffix.lower()
        
        # 1. Validate file extension
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning(f"Rejected upload due to invalid extension: {ext}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file extension '{ext}'. Supported extensions are: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        # 2. Validate MIME type
        mime_type = file.content_type
        if mime_type not in ALLOWED_MIME_TYPES:
            logger.warning(f"Rejected upload due to invalid content-type: {mime_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported content type '{mime_type}'. Supported types are: PDF, DOCX, JPEG, PNG"
            )

        # 3. Validate file size
        try:
            # Check size by seeking
            await file.seek(0, 2)
            size = await file.tell()
            await file.seek(0)
        except Exception as e:
            logger.error(f"Error calculating file size via seek: {str(e)}")
            # Fallback
            content = await file.read()
            size = len(content)
            await file.seek(0)

        if size > MAX_FILE_SIZE:
            logger.warning(f"Rejected upload due to size limit: {size} bytes")
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds the 20MB limit. Uploaded file size: {size / (1024 * 1024):.2f}MB"
            )

        # 4. Generate unique UUID filename
        unique_filename = f"{uuid.uuid4()}{ext}"
        filepath = UPLOADS_DIR / unique_filename

        # Ensure directory exists
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

        # 5. Save file contents in chunks (prevent memory bloat)
        try:
            logger.info(f"Saving uploaded file '{filename}' to '{filepath}' (Size: {size} bytes)...")
            with open(filepath, "wb") as f:
                while chunk := await file.read(1024 * 1024):  # 1MB chunk size
                    f.write(chunk)
        except Exception as e:
            logger.error(f"Error saving file to disk: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error saving file: {str(e)}"
            )

        return {
            "success": True,
            "filename": unique_filename,
            "filepath": str(filepath),
            "filetype": mime_type,
            "size": size
        }
