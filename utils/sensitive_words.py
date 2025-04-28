from __future__ import annotations

import os
import yaml
from functools import lru_cache
from typing import Dict, List

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
KEYWORD_FILE = os.path.join(BASE_DIR, "config", "sensitive_keywords.yaml")


@lru_cache()
def _load_yaml() -> Dict[str, List[str]]:
    if not os.path.exists(KEYWORD_FILE):
        raise FileNotFoundError(
            f"Keyword file not found: {KEYWORD_FILE}. "
            "Please create it first."
        )
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {cat: [w.lower() for w in words] for cat, words in data.items()}


def load_sensitive_dict(refresh: bool = False) -> Dict[str, List[str]]:
    if refresh:
        _load_yaml.cache_clear()
    return _load_yaml()


def check_text(text: str | None) -> Dict[str, List[str]]:
    if not text:
        return {}

    text_lower = text.lower()
    hits: Dict[str, List[str]] = {}

    for category, words in load_sensitive_dict().items():
        matched = [w for w in words if w in text_lower]
        if matched:
            hits[category] = matched

    return hits
