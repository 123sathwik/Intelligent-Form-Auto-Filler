import numpy as np

class SimilarityEngine:
    @staticmethod
    def cosine_similarity(v1: list, v2: list) -> float:
        """
        Computes cosine similarity between two 1D vector arrays.
        """
        a = np.array(v1)
        b = np.array(v2)
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))
