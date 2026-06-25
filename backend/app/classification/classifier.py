import re
import joblib
import logging
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from app.ml.embedding_service import EmbeddingService
from app.classification.dataset import DocumentDatasetGenerator

logger = logging.getLogger("autofiller-backend")

MODELS_DIR = Path("c:/Users/Admin/OneDrive/auto filler/backend/models")
MODEL_PATH = MODELS_DIR / "document_classifier.joblib"
ENCODER_PATH = MODELS_DIR / "document_classifier_encoder.joblib"

KEYWORDS_MAP = {
    "Resume": ["resume", "cv", "skills", "experience", "projects", "education", "technologies", "summary"],
    "Passport": ["passport", "republic", "surname", "nationality", "given names", "expiry", "authority", "travel"],
    "Aadhaar": ["aadhaar", "uidai", "unique identification", "mera aadhaar", "pehchan", "government of india"],
    "PAN Card": ["permanent account number", "income tax", "pan card", "tax department", "govt of india"],
    "Driving License": ["driving licence", "driving license", "licence number", "license number", "lmv", "mcwg", "licensing authority"],
    "Invoice": ["invoice", "bill to", "subtotal", "due date", "po number", "tax id", "total amount", "vendor", "invoice number"],
    "Bank Statement": ["bank statement", "account statement", "statement period", "closing balance", "opening balance", "withdrawals", "deposits", "account holder"],
    "Medical Report": ["medical report", "patient name", "patient id", "diagnosis", "symptoms", "recommendations", "tests performed", "clinical summary"],
    "Research Paper": ["abstract", "introduction", "methodology", "references", "doi", "arxiv", "keywords", "conclusion", "authors"],
    "Egg AI Report": ["egg inspection", "egg quality", "grade a eggs", "grade b eggs", "reject count", "humidity", "temperature", "poultry tech"],
    "Certificate": ["certificate of", "successfully completed", "credential id", "completion", "achievement", "awarded to", "certified"],
    "Generic Document": ["general", "memo", "subject", "meeting notes", "memorandum", "update", "author"]
}

class DocumentClassifier:
    _model = None
    _encoder = None

    @classmethod
    def get_resources(cls):
        """
        Loads the classifier model and label encoder from disk (or trains them if not present).
        """
        if cls._model is None or cls._encoder is None:
            MODELS_DIR.mkdir(parents=True, exist_ok=True)
            if not MODEL_PATH.exists() or not ENCODER_PATH.exists():
                logger.info("Classifier model or encoder not found. Training document classifier model...")
                cls.train_classifier()
            else:
                try:
                    cls._model = joblib.load(str(MODEL_PATH))
                    cls._encoder = joblib.load(str(ENCODER_PATH))
                    logger.info("Loaded document classifier and encoder from disk.")
                except Exception as e:
                    logger.error(f"Error loading classifier: {e}. Retraining...")
                    cls.train_classifier()
        return cls._model, cls._encoder

    @classmethod
    def extract_features(cls, text: str) -> np.ndarray:
        """
        Computes features for a given input text:
        - 384 dimensional sentence embedding
        - Layout statistics (text length, word count, line count, average line length, numeric ratio)
        - Regex match flags (Aadhaar, PAN, Passport, Phone, Email, Currency)
        - Keyword counts for all categories
        """
        text_lower = text.lower()

        # 1. Embeddings
        embedding = EmbeddingService.get_embedding(text)

        # 2. Layout Statistics
        char_len = len(text)
        words = text.split()
        word_count = len(words)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        line_count = len(lines)
        avg_line_len = sum(len(line) for line in lines) / (line_count if line_count > 0 else 1)
        numeric_count = sum(c.isdigit() for c in text)
        numeric_ratio = numeric_count / (char_len if char_len > 0 else 1)

        # 3. Regex Patterns
        has_aadhaar = 1.0 if re.search(r"\d{4}\s\d{4}\s\d{4}", text) else 0.0
        has_pan = 1.0 if re.search(r"[A-Z]{5}\d{4}[A-Z]", text) else 0.0
        has_passport = 1.0 if re.search(r"[A-Z]\d{7}", text) else 0.0
        has_email = 1.0 if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text) else 0.0
        has_phone = 1.0 if re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text) else 0.0
        has_currency = 1.0 if re.search(r"(\$|INR|Rs\.|USD|EUR)", text) else 0.0

        layout_feats = [
            char_len / 1000.0,
            word_count / 200.0,
            line_count / 20.0,
            avg_line_len / 50.0,
            numeric_ratio,
            has_aadhaar,
            has_pan,
            has_passport,
            has_email,
            has_phone,
            has_currency
        ]

        # 4. Keyword Features
        keyword_feats = []
        for category, keywords in KEYWORDS_MAP.items():
            count = sum(text_lower.count(kw) for kw in keywords)
            keyword_feats.append(float(count))

        # Concatenate all features
        features = np.concatenate([
            np.array(embedding),
            np.array(layout_feats),
            np.array(keyword_feats)
        ])
        return features

    @classmethod
    def train_classifier(cls):
        """
        Trains the RandomForestClassifier on the generated dataset and saves it to disk.
        """
        logger.info("Generating training samples for document classifier...")
        samples = DocumentDatasetGenerator.generate_raw_samples()
        
        X_list = []
        y_raw = []
        for text, label in samples:
            feats = cls.extract_features(text)
            X_list.append(feats)
            y_raw.append(label)

        X = np.array(X_list)

        cls._encoder = LabelEncoder()
        y = cls._encoder.fit_transform(y_raw)

        logger.info(f"Training Random Forest on {len(X)} instances with feature size {X.shape[1]}...")
        cls._model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        cls._model.fit(X, y)

        # Save to disk
        joblib.dump(cls._model, str(MODEL_PATH))
        joblib.dump(cls._encoder, str(ENCODER_PATH))
        logger.info(f"Saved trained classifier to {MODEL_PATH}")
        logger.info(f"Saved label encoder to {ENCODER_PATH}")

    @classmethod
    def classify(cls, text: str) -> dict:
        """
        Classifies the input text and returns predicted label and confidence score.
        """
        if not text or not text.strip():
            return {
                "document_type": "Generic Document",
                "confidence": 100.0
            }

        model, encoder = cls.get_resources()

        # Extract features
        feats = cls.extract_features(text).reshape(1, -1)

        # Predict
        probs = model.predict_proba(feats)[0]
        pred_idx = np.argmax(probs)
        confidence = float(probs[pred_idx]) * 100.0
        predicted_label = str(encoder.inverse_transform([pred_idx])[0])

        return {
            "document_type": predicted_label,
            "confidence": round(confidence, 1)
        }
