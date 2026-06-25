import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("autofiller-backend")

_model = None

class EmbeddingService:
    @staticmethod
    def get_model() -> SentenceTransformer:
        """
        Loads and returns the SentenceTransformer singleton.
        """
        global _model
        if _model is None:
            logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
            try:
                _model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.error(f"Failed to load SentenceTransformer: {str(e)}")
                raise RuntimeError(f"SentenceTransformer not loaded: {str(e)}")
        return _model

    @staticmethod
    def get_embedding(text: str) -> list:
        """
        Generates a 384-dimensional embedding for a single text label.
        """
        if not text:
            return [0.0] * 384
        model = EmbeddingService.get_model()
        embedding = model.encode(text)
        return embedding.tolist()

    @staticmethod
    def get_embeddings(texts: list) -> list:
        """
        Generates embeddings for a list of text labels.
        """
        if not texts:
            return []
        model = EmbeddingService.get_model()
        embeddings = model.encode(texts)
        return embeddings.tolist()
