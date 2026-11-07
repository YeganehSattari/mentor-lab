"""Run policies on many seeds and report robust statistics (IQM + percentile bootstrap CI), as in Agarwal et al. 2021."""
from __future__ import annotations

import statistics
from typing import Callable

from .env import InternSim
from .seeds import rng


def run_episode(make_policy: Callable[[int], object], seed: int) -> dict[str, float]:
    env = InternSim(); ctx = env.reset(seed); pol = make_policy(seed)
    total = cost = 0.0; done = False
    while not done:
        chosen = pol.select(ctx, env.k)
        nxt, rwd, c, done = env.step(chosen)
        per = [1.0 if env.interns[i].inactive == 0 else 0.0 for i in chosen]
        pol.update(ctx, chosen, per)
        total += rwd; cost += c; ctx = nxt
    return {"return": total, "cost": cost}


def iqm(xs: list[float]) -> float:
    s = sorted(xs); n = len(s); lo, hi = n // 4, n - n // 4
    return statistics.fmean(s[lo:hi] or s)


def bootstrap_ci(xs: list[float], stat=iqm, b: int = 2000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    r = rng(seed, "bootstrap"); vals = sorted(stat([r.choice(xs) for _ in xs]) for _ in range(b))
    return vals[int(b * alpha / 2)], vals[int(b * (1 - alpha / 2)) - 1]


def evaluate(make_policy: Callable[[int], object], seeds: list[int]) -> dict[str, object]:
    runs = [run_episode(make_policy, s) for s in seeds]
    ret = [x["return"] for x in runs]; cost = [x["cost"] for x in runs]
    return {"iqm": iqm(ret), "ci": bootstrap_ci(ret), "mean_cost": statistics.fmean(cost), "returns": ret}
