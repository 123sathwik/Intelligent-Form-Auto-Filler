import numpy as np
import logging
from app.ml.embedding_service import EmbeddingService

logger = logging.getLogger("autofiller-backend")

class FeatureBuilder:
    @staticmethod
    def build_features(texts: list) -> np.ndarray:
        """
        Converts raw text labels into a feature matrix X of shape (N, 384)
        consisting of semantic embeddings.
        """
        logger.info(f"Generating feature embeddings for {len(texts)} texts...")
        embeddings = EmbeddingService.get_embeddings(texts)
        return np.array(embeddings)
