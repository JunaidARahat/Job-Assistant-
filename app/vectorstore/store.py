from typing import List, Dict
import numpy as np

class VectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.ids = []
        self.texts = []
        self.vectors = None
        self.use_faiss = False
        try:
            import faiss
            self.faiss = faiss
            self.index = None
            self.use_faiss = True
        except Exception:
            self.index = None

    def add_documents(self, ids: List[str], texts: List[str]):
        vecs = np.array(self.embedding_model.embed(texts))
        if self.use_faiss:
            d = vecs.shape[1]
            if self.index is None:
                self.index = self.faiss.IndexFlatIP(d)
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            vecs_norm = (vecs / norms).astype('float32')
            self.index.add(vecs_norm)
        else:
            if self.vectors is None:
                self.vectors = vecs
            else:
                self.vectors = np.vstack([self.vectors, vecs])

        self.ids.extend(ids)
        self.texts.extend(texts)

    def search(self, query: str, k: int = 3):
        qv = np.array(self.embedding_model.embed([query]))[0]
        if self.use_faiss and self.index is not None:
            import numpy as _np
            qn = qv / (np.linalg.norm(qv) + 1e-9)
            D, I = self.index.search(_np.array([qn]).astype('float32'), k)
            out = []
            for idx in I[0]:
                if 0 <= idx < len(self.texts):
                    out.append({'id': self.ids[idx], 'text': self.texts[idx]})
            return out
        else:
            if self.vectors is None:
                return []
            sims = self.vectors.dot(qv) / (np.linalg.norm(self.vectors, axis=1) * (np.linalg.norm(qv) + 1e-9) + 1e-9)
            top = sims.argsort()[::-1][:k]
            return [{'id': self.ids[i], 'text': self.texts[i], 'score': float(sims[i])} for i in top]
