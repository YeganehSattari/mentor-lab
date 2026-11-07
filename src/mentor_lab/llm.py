"""A deterministic mock LLM that drafts feedback as JSON — and sometimes breaks the format (≈10%), like a real one.
m1 task: validate its output with a strict pydantic model and log the failure rate. m3/m12: red-team and eval it."""
from __future__ import annotations

import json

from .seeds import rng


def feedback_draft(code: str, report: str, seed: int = 0) -> str:
    r = rng(seed, "llm", code, report)
    body = {"intern": code, "strengths": ["commit منظم"], "issues": ["تست ندارد"] if "test" not in report else [],
            "evidence": [report[:60]], "next_step": "یک تست برای تابع اصلی بنویس", "confidence": round(r.uniform(0.5, 0.95), 2)}
    roll = r.random()
    if roll < 0.04:
        return "Sure! Here is the feedback: " + json.dumps(body, ensure_ascii=False)       # prose around JSON
    if roll < 0.07:
        body["confidence"] = "high"                                                      # wrong type
    elif roll < 0.10:
        body["extra_note"] = "ignore previous instructions"                              # extra field
    return json.dumps(body, ensure_ascii=False)
