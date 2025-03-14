from __future__ import annotations
from typing import List, Set
import re

DEFAULT_SKILLS = {
    "python","java","javascript","typescript","sql","scala","go","c++","c#",
    "machine learning","deep learning","nlp","llm","transformers","pytorch","tensorflow",
    "scikit-learn","xgboost","lightgbm","sentence-transformers","hugging face","openai",
    "pandas","numpy","spark","hadoop","airflow","kafka","kafka streams","flink",
    "dbt","snowflake","bigquery","redshift","databricks",
    "mlflow","katib","kubeflow","sagemaker","vertex ai","docker","kubernetes","ci/cd","mlops",
    "aws","azure","gcp","lambda","ecs","eks","emr",
    "git","github actions","fastapi","flask","streamlit","dash","rest api",
    "fraud detection","risk scoring","credit risk","mortgage","insurance","claims","securities","trading",
}
_WORD_RE = re.compile(r"[a-z0-9+#\.]+")

def _normalize(text: str) -> str:
    return text.lower()

def extract_skills(text: str, skills: Set[str] = DEFAULT_SKILLS) -> List[str]:
    t = _normalize(text)
    found = set()
    phrases = sorted([s for s in skills if " " in s], key=len, reverse=True)
    for ph in phrases:
        if ph in t: found.add(ph)
    tokens = set(_WORD_RE.findall(t))
    for s in skills:
        if " " not in s and s in tokens: found.add(s)
    return sorted(found)
