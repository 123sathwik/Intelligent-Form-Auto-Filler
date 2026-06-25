import logging
from pathlib import Path

logger = logging.getLogger("autofiller-backend")

# Global EasyOCR reader instance (lazy initialized singleton)
reader = None

def get_easyocr_reader():
    global reader
    if reader is None:
        try:
            import easyocr  # lazy import
        except ImportError as e:
            logger.error(f"Failed to import easyocr: {str(e)}")
            raise ImportError("OCR dependencies are not installed.")
            
        logger.info("Initializing EasyOCR Reader...")
        try:
            # Initialize reader
            reader = easyocr.Reader(['en'], gpu=False)
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {str(e)}")
            raise e
    return reader

class ImageExtractor:
    @staticmethod
    def preprocess_image(file_path: Path):
        """
        Preprocesses an image for OCR:
        - Grayscale conversion
        - Contrast enhancement (CLAHE)
        - Denoising (Gaussian Blur)
        - Otsu thresholding (binarization)
        - Deskewing (rotational correction up to 15 degrees)
        """
        try:
            import cv2
            import numpy as np
        except ImportError as e:
            logger.error(f"Failed to import cv2 or numpy: {str(e)}")
            raise ImportError("OCR dependencies are not installed.")

        logger.info(f"Preprocessing image: {file_path}")
        
        # Read image
        img = cv2.imread(str(file_path))
        if img is None:
            raise ValueError(f"Could not load image file: {file_path}")

        # 1. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Increase contrast (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast = clahe.apply(gray)

        # 3. Remove noise (Gaussian Blur)
        denoised = cv2.GaussianBlur(contrast, (3, 3), 0)

        # 4. Threshold (Otsu's thresholding)
        thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # 5. Deskew
        # Look at corners to determine background color
        h, w = thresholded.shape[:2]
        corners = [
            thresholded[0, 0], 
            thresholded[0, w - 1], 
            thresholded[h - 1, 0], 
            thresholded[h - 1, w - 1]
        ]
        bg_is_white = sum(corners) > 510  # If at least 2 corners are white (255)

        # Invert if bg is white, so that text is white (non-zero) for findNonZero
        fg = cv2.bitwise_not(thresholded) if bg_is_white else thresholded
        
        pts = cv2.findNonZero(fg)
        processed_img = thresholded
        
        if pts is not None:
            rect = cv2.minAreaRect(pts)
            angle = rect[-1]
            
            # Normalize angle
            if angle < -45:
                angle = -(90 + angle)
            elif angle > 45:
                angle = 90 - angle

            # Apply correction only if rotation is minor but significant (0.5 to 15 degrees)
            if 0.5 < abs(angle) < 15.0:
                logger.info(f"Deskewing image by angle: {angle:.2f} degrees")
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                processed_img = cv2.warpAffine(
                    thresholded, 
                    M, 
                    (w, h), 
                    flags=cv2.INTER_CUBIC, 
                    borderMode=cv2.BORDER_REPLICATE
                )

        return processed_img

    @staticmethod
    def extract(file_path: Path) -> dict:
        """
        Runs image preprocessing, executes EasyOCR, and returns combined text.
        """
        try:
            # Preprocess the image (triggers cv2/numpy imports)
            preprocessed = ImageExtractor.preprocess_image(file_path)
            
            # Fetch EasyOCR reader (triggers easyocr import)
            ocr_reader = get_easyocr_reader()
            
            # Run EasyOCR text detection
            logger.info("Executing EasyOCR text recognition...")
            results = ocr_reader.readtext(preprocessed)
            
            # Extract and join text components
            extracted_text = "\n".join([res[1] for res in results])
            
            return {
                "text": extracted_text,
                "pages": 1,
                "metadata": {},
                "extractor": "opencv-easyocr"
            }
        except ImportError as e:
            # Re-raise to be handled by the service/endpoint layer
            raise e
        except Exception as e:
            logger.error(f"Image text extraction failed: {str(e)}")
            raise e
