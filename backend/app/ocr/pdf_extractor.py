import logging
from pathlib import Path

logger = logging.getLogger("autofiller-backend")

class PDFExtractor:
    @staticmethod
    def extract(file_path: Path) -> dict:
        """
        Extracts text, page count, and metadata from a PDF file.
        Primary: PyMuPDF. Fallback: pdfplumber.
        """
        import fitz  # PyMuPDF (lazy import)
        
        try:
            logger.info(f"Attempting PDF extraction via PyMuPDF for: {file_path}")
            doc = fitz.open(str(file_path))
            page_count = len(doc)
            
            # Extract metadata
            metadata = {
                "author": doc.metadata.get("author", "") if doc.metadata else "",
                "creator": doc.metadata.get("creator", "") if doc.metadata else "",
                "producer": doc.metadata.get("producer", "") if doc.metadata else "",
                "subject": doc.metadata.get("subject", "") if doc.metadata else "",
                "title": doc.metadata.get("title", "") if doc.metadata else "",
                "keywords": doc.metadata.get("keywords", "") if doc.metadata else "",
                "creationDate": doc.metadata.get("creationDate", "") if doc.metadata else "",
                "modDate": doc.metadata.get("modDate", "") if doc.metadata else ""
            }

            text_content = []
            for page in doc:
                text_content.append(page.get_text() or "")

            full_text = "\n".join(text_content)
            doc.close()
            
            # If PyMuPDF returned completely empty text, fallback to pdfplumber
            if not full_text.strip():
                logger.warning("PyMuPDF returned empty text. Falling back to pdfplumber...")
                return PDFExtractor._extract_with_pdfplumber(file_path)

            return {
                "text": full_text,
                "pages": page_count,
                "metadata": metadata,
                "extractor": "pymupdf"
            }
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {str(e)}. Attempting fallback to pdfplumber...")
            try:
                return PDFExtractor._extract_with_pdfplumber(file_path)
            except Exception as fe:
                logger.error(f"Fallback pdfplumber extraction failed as well: {str(fe)}")
                raise fe

    @staticmethod
    def _extract_with_pdfplumber(file_path: Path) -> dict:
        import pdfplumber  # pdfplumber (lazy import)
        
        logger.info(f"Running pdfplumber extraction for: {file_path}")
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            
            # Extract metadata
            metadata = pdf.metadata or {}
            
            text_content = []
            for page in pdf.pages:
                text_content.append(page.extract_text() or "")
                
            full_text = "\n".join(text_content)
            
            return {
                "text": full_text,
                "pages": page_count,
                "metadata": metadata,
                "extractor": "pdfplumber"
            }
