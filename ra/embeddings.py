from __future__ import annotations
from typing import List
import functools, numpy as np

@functools.lru_cache(maxsize=2)
def ensure_model(model_name: str):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)

def embed_texts(texts: List[str], model) -> np.ndarray:
    return np.array(model.encode(texts, convert_to_numpy=True, normalize_embeddings=True))
