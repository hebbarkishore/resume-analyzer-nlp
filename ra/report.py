from __future__ import annotations
from typing import Dict, Any, List
def build_report(*, resume_text: str, jd_text: str, model: str, similarity: float,
                 top_matches: List[dict], skills: Dict[str, list]) -> Dict[str, Any]:
    return {
        "model": model,
        "similarity": round(similarity, 4),
        "skills": skills,
        "top_sentence_matches": top_matches,
        "meta": {"resume_chars": len(resume_text), "jd_chars": len(jd_text)},
    }
