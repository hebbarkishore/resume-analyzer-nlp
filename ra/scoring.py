from __future__ import annotations
from typing import List, Tuple
import numpy as np, pandas as pd, re

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9])')
def split_sentences(text: str, max_len: int = 400) -> List[str]:
    parts = _SENT_SPLIT.split(text)
    out = []
    for p in parts:
        p = p.strip()
        if not p: continue
        while len(p) > max_len:
            out.append(p[:max_len]); p = p[max_len:]
        out.append(p)
    return out[:200]

def top_sentence_matches(resume_text: str, jd_text: str, model, top_k: int = 8) -> pd.DataFrame:
    from ra.embeddings import embed_texts
    res_sents = split_sentences(resume_text)
    jd_sents = split_sentences(jd_text)
    if not res_sents or not jd_sents:
        return pd.DataFrame(columns=["resume_sentence", "jd_sentence", "similarity"])
    res_emb = embed_texts(res_sents, model)
    jd_emb = embed_texts(jd_sents, model)
    sims = res_emb @ jd_emb.T
    pairs: List[Tuple[str, str, float]] = []
    for i, row in enumerate(sims):
        j = int(np.argmax(row))
        pairs.append((res_sents[i], jd_sents[j], float(row[j])))
    pairs.sort(key=lambda x: x[2], reverse=True)
    top = pairs[:top_k]
    return pd.DataFrame([{"resume_sentence": a, "jd_sentence": b, "similarity": round(s, 3)} for a, b, s in top])
