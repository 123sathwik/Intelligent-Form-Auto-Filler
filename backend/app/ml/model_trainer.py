import os
import joblib
import logging
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

from app.ml.dataset_generator import DatasetGenerator
from app.ml.feature_builder import FeatureBuilder

logger = logging.getLogger("autofiller-backend")

# Models directory path
MODELS_DIR = Path("c:/Users/Admin/OneDrive/auto filler/backend/models")

class ModelTrainer:
    @staticmethod
    def train_and_evaluate() -> dict:
        """
        Runs the training pipeline:
        1. Generates dataset.
        2. Generates feature embeddings.
        3. Encodes labels.
        4. Trains and evaluates Random Forest and XGBoost.
        5. Saves the best model to disk.
        """
        logger.info("Initializing model training pipeline...")
        MODELS_DIR.mkdir(parents=True, exist_ok=True)

        # 1. Generate Dataset
        texts, raw_labels = DatasetGenerator.generate()
        logger.info(f"Generated dataset with {len(texts)} instances.")

        # 2. Encode Labels
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(raw_labels)

        # 3. Generate Features
        X = FeatureBuilder.build_features(texts)

        # 4. Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        logger.info(f"Train set size: {len(X_train)}, Test set size: {len(X_test)}")

        # 5. Train Random Forest
        logger.info("Training Random Forest Classifier...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(X_train, y_train)
        rf_preds = rf_model.predict(X_test)
        rf_accuracy = float(accuracy_score(y_test, rf_preds))
        logger.info(f"Random Forest validation accuracy: {rf_accuracy:.4f}")

        # 6. Train XGBoost
        logger.info("Training XGBoost Classifier...")
        xgb_model = XGBClassifier(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=6, 
            random_state=42, 
            n_jobs=-1,
            eval_metric="mlogloss"
        )
        xgb_model.fit(X_train, y_train)
        xgb_preds = xgb_model.predict(X_test)
        xgb_accuracy = float(accuracy_score(y_test, xgb_preds))
        logger.info(f"XGBoost validation accuracy: {xgb_accuracy:.4f}")

        # 7. Compare and Save Best Model
        best_model = None
        best_name = ""
        best_accuracy = 0.0

        if xgb_accuracy >= rf_accuracy:
            best_model = xgb_model
            best_name = "XGBoost"
            best_accuracy = xgb_accuracy
        else:
            best_model = rf_model
            best_name = "RandomForest"
            best_accuracy = rf_accuracy

        logger.info(f"Selected {best_name} as the best model with accuracy {best_accuracy:.4f}")

        # Save artifacts
        model_path = MODELS_DIR / "field_mapping_model.joblib"
        encoder_path = MODELS_DIR / "label_encoder.joblib"
        
        joblib.dump(best_model, str(model_path))
        joblib.dump(label_encoder, str(encoder_path))
        
        logger.info(f"Saved best model to: {model_path}")
        logger.info(f"Saved label encoder to: {encoder_path}")

        return {
            "best_model_name": best_name,
            "best_accuracy": best_accuracy,
            "rf_accuracy": rf_accuracy,
            "xgb_accuracy": xgb_accuracy,
            "model_path": str(model_path),
            "encoder_path": str(encoder_path)
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ModelTrainer.train_and_evaluate()
