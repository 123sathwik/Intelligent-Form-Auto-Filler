import time
import logging
from pathlib import Path
from fastapi import HTTPException

from app.ocr.pdf_extractor import PDFExtractor
from app.ocr.docx_extractor import DOCXExtractor
from app.ocr.image_extractor import ImageExtractor
from app.ocr.text_cleaner import TextCleaner
from app.services.document_service import UPLOADS_DIR

logger = logging.getLogger("autofiller-backend")

class OCRService:
    @staticmethod
    async def extract_text(filename: str) -> dict:
        """
        Coordinates text extraction:
        1. Checks if file exists
        2. Resolves file type
        3. Dispatches to matching extractor (PDF, DOCX, Image)
        4. Applies TextCleaner
        5. Catch ImportError (missing/incompatible cv2/easyocr) and returns clean error response
        6. Logs metrics (processing time, pages, state changes)
        """
        # Resolve target path
        file_path = UPLOADS_DIR / filename
        
        # Validate existence
        if not file_path.exists() or not file_path.is_file():
            logger.error(f"Missing file error: Uploaded file '{filename}' not found at: {file_path}")
            raise HTTPException(
                status_code=404, 
                detail=f"Uploaded file '{filename}' not found on the server. Please upload it first."
            )

        ext = file_path.suffix.lower()
        file_type = ext.replace(".", "")

        logger.info(f"File received for text extraction: '{filename}' (Type: {file_type})")
        logger.info(f"OCR/Extraction started for file: {filename}")
        
        start_time = time.time()
        
        try:
            if ext == ".pdf":
                result = PDFExtractor.extract(file_path)
            elif ext == ".docx":
                result = DOCXExtractor.extract(file_path)
            elif ext in [".jpg", ".jpeg", ".png"]:
                result = ImageExtractor.extract(file_path)
            else:
                logger.error(f"Unsupported file format for text extraction: {ext}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file type '{ext}' for text extraction. Supported types: PDF, DOCX, JPG, JPEG, PNG."
                )
        except ImportError as e:
            # Handle missing OCR dependencies gracefully without crashing or throwing HTTP 500
            logger.error(f"OCR dependencies missing/incompatible while processing '{filename}': {str(e)}")
            return {
                "success": False,
                "message": "OCR dependencies are not installed."
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"OCR/Extraction failure for file '{filename}': {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"OCR or text extraction process failed: {str(e)}"
            )

        # Calculate metrics
        duration = time.time() - start_time
        pages = result.get("pages", 1)
        raw_text = result.get("text", "")
        
        # Clean text
        cleaned_text = TextCleaner.clean(raw_text)
        
        logger.info(f"OCR/Extraction completed for file: {filename}")
        logger.info(f"Extraction metrics: [Duration: {duration:.3f}s] [Pages processed: {pages}]")

        return {
            "success": True,
            "file_type": file_type,
            "pages": pages,
            "text": cleaned_text
        }
