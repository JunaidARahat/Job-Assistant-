from typing import List
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = None):
        self.backend = 'mock'
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer
            mname = model_name or 'all-MiniLM-L6-v2'
            self.model = SentenceTransformer(mname)
            self.backend = 'sbert'
        except Exception:
            self.backend = 'mock'

    def embed(self, texts: List[str]):
        if not isinstance(texts, list):
            texts = [texts]
        if self.backend == 'sbert' and self.model is not None:
            arr = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
            return [a.tolist() for a in arr]
        else:
            return [self._mock_embed(t) for t in texts]

    def _mock_embed(self, text: str, dim: int = 128):
        v = np.zeros(dim, dtype=float)
        for i, b in enumerate(text.encode('utf8')):
            v[i % dim] += b
        norm = np.linalg.norm(v)
        if norm > 0:
            v = (v / norm).tolist()
        else:
            v = v.tolist()
        return v
