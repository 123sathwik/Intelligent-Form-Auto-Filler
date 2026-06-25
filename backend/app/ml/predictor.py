import joblib
import numpy as np
import logging
from pathlib import Path
from app.ml.embedding_service import EmbeddingService

logger = logging.getLogger("autofiller-backend")

# Models directory path
MODELS_DIR = Path("c:/Users/Admin/OneDrive/auto filler/backend/models")

_model = None
_encoder = None

class Predictor:
    @staticmethod
    def load_artifacts():
        """Loads classifier and label encoder model artifacts from disk on demand."""
        global _model, _encoder
        if _model is None or _encoder is None:
            model_path = MODELS_DIR / "field_mapping_model.joblib"
            encoder_path = MODELS_DIR / "label_encoder.joblib"
            
            # Automatically run training pipeline if artifacts are not found
            if not model_path.exists() or not encoder_path.exists():
                logger.info("Model artifacts not found on disk. Initiating auto-training...")
                from app.ml.model_trainer import ModelTrainer
                ModelTrainer.train_and_evaluate()
                
            logger.info("Loading model artifacts from disk...")
            _model = joblib.load(str(model_path))
            _encoder = joblib.load(str(encoder_path))

    @staticmethod
    def predict(label: str) -> tuple:
        """
        Predicts the standard intermediate schema field for a single unknown label.
        Returns a tuple of (predicted_class_name, confidence_score).
        """
        if not label or not label.strip():
            return "name", 0.0
            
        Predictor.load_artifacts()
        
        # 1. Embed single string
        embedding = EmbeddingService.get_embedding(label)
        
        # 2. Compute prediction probability distribution
        # Both RandomForest and XGBoost classifiers implement predict_proba
        probs = _model.predict_proba([embedding])[0]
        
        # 3. Decode index and max probability
        pred_idx = int(np.argmax(probs))
        confidence = float(probs[pred_idx])
        class_name = str(_encoder.inverse_transform([pred_idx])[0])
        
        return class_name, confidence

    @staticmethod
    def predict_batch(labels: list) -> list:
        """
        Runs batch predictions for a list of unknown labels.
        Returns list of (predicted_class_name, confidence_score) tuples.
        """
        if not labels:
            return []
            
        Predictor.load_artifacts()
        
        # 1. Batch encode
        embeddings = EmbeddingService.get_embeddings(labels)
        
        # 2. Get batch probabilities
        preds_probs = _model.predict_proba(embeddings)
        
        # 3. Decode results
        results = []
        for probs in preds_probs:
            pred_idx = int(np.argmax(probs))
            confidence = float(probs[pred_idx])
            class_name = str(_encoder.inverse_transform([pred_idx])[0])
            results.append((class_name, confidence))
            
        return results
