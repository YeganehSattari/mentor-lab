"""InternSim — a toy but non-trivial model of a cohort and of daily mentor feedback.

Each day the mentor (the policy) chooses K interns to give feedback to. Hidden state per intern:
  mastery  ∈ [0,1]   (BKT-like, rises with practice)
  motive   ∈ [0,1]   (drops when ignored, rises after good feedback)
  gap      int       (days since last feedback)
Observed context per intern (what a real bot can see):
  [1, days_inactive/7, commits_3d/5, last_quiz, gap/7, feedback_7d/3]
Reward for the day = number of interns who were active the next day (0..N).
Cost for the day   = number of interns whose gap exceeds MAX_GAP (fairness constraint, CMDP-style).
Feedback works best in the "zone of proximal development": interns with medium mastery and falling motivation.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

from .seeds import rng

N_INTERNS = 12
K = 3
MAX_GAP = 4
HORIZON = 30
CODES = [f"H-{i:02d}" for i in range(1, N_INTERNS + 1)]


@dataclass
class Intern:
    code: str
    mastery: float
    motive: float
    gap: int = 0
    inactive: int = 0
    commits3: list[int] = field(default_factory=lambda: [0, 0, 0])
    last_quiz: float = 0.5
    fb7: list[int] = field(default_factory=lambda: [0] * 7)


def _sig(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


class InternSim:
    def __init__(self, n: int = N_INTERNS, k: int = K, horizon: int = HORIZON, max_gap: int = MAX_GAP):
        self.n, self.k, self.horizon, self.max_gap = n, k, horizon, max_gap
        self.t = 0
        self.interns: list[Intern] = []
        self.r = rng(0, "unset")

    def reset(self, seed: int) -> list[list[float]]:
        init = rng(seed, "init")
        self.r = rng(seed, "dynamics")
        self.t = 0
        self.interns = [Intern(c, mastery=init.uniform(0.05, 0.6), motive=init.uniform(0.4, 0.95)) for c in CODES[: self.n]]
        return self.contexts()

    def contexts(self) -> list[list[float]]:
        return [[1.0, i.inactive / 7, sum(i.commits3) / 5, i.last_quiz, i.gap / 7, sum(i.fb7) / 3] for i in self.interns]

    def step(self, chosen: Sequence[int]) -> tuple[list[list[float]], float, float, bool]:
        assert len(set(chosen)) == len(chosen) <= self.k, "choose at most k distinct interns"
        active_next = 0
        for idx, it in enumerate(self.interns):
            got = idx in chosen
            if got:
                zpd = 1.0 - abs(it.mastery - 0.45) * 2          # best around medium mastery
                need = 1.0 - it.motive                            # helps most when motivation dropped
                it.motive = min(1.0, it.motive + 0.15 * zpd + 0.2 * need)
                it.gap = 0
            else:
                it.gap += 1
                it.motive = max(0.0, it.motive - 0.03 * max(0, it.gap - 1))
            it.fb7 = it.fb7[1:] + [1 if got else 0]
            p_active = _sig(4 * it.motive - 1.5 - 0.15 * it.inactive)
            active = self.r.random() < p_active
            commits = self.r.randint(1, 3) if active else 0
            if active:
                active_next += 1
                it.inactive = 0
                it.mastery = min(1.0, it.mastery + 0.03 * (1 - it.mastery) * (1.5 if got else 1.0))
                if self.r.random() < 0.3:
                    it.last_quiz = min(1.0, max(0.0, it.mastery + self.r.gauss(0, 0.1)))
            else:
                it.inactive += 1
            it.commits3 = it.commits3[1:] + [commits]
        cost = float(sum(1 for it in self.interns if it.gap > self.max_gap))
        self.t += 1
        return self.contexts(), float(active_next), cost, self.t >= self.horizon
