from __future__ import annotations
import logging
from pydantic import BaseModel, ConfigDict, ValidationError
from .llm import feedback_draft

log = logging.getLogger("mentor_lab.llm")


class FeedbackDraft(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    intern: str
    strengths: list[str]
    issues: list[str]
    evidence: list[str]
    next_step: str
    confidence: float


def parse_draft(raw: str) -> FeedbackDraft:
    return FeedbackDraft.model_validate_json(raw, strict=True)


def format_failure_rate(n: int = 1000) -> float:
    failures = 0
    for i in range(n):
        raw = feedback_draft(f"H-{i % 12 + 1:02d}", f"commit {i}: refactor", seed=i)
        try:
            parse_draft(raw)
        except ValidationError as e:
            failures += 1
            log.warning("format failure #%d: %s", i, e.errors()[0]["type"])
    rate = failures / n
    log.info("format failure rate: %d/%d = %.1f%%", failures, n, 100 * rate)
    return rate