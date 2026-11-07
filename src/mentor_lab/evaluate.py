"""Run policies on many seeds and report robust statistics (IQM + percentile bootstrap CI), as in Agarwal et al. 2021."""
from __future__ import annotations

import asyncio
import logging
import random
import statistics
from typing import Callable

from .env import InternSim
from .protocols import Context, Policy
from .seeds import derive_seed, rng

log = logging.getLogger("mentor_lab.eval")

PolicyFactory = Callable[[int], Policy[Context, int]]


def run_episode(make_policy: PolicyFactory, seed: int) -> dict[str, float]:
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


def bootstrap_ci(xs: list[float], stat: Callable[[list[float]], float] = iqm, b: int = 2000, alpha: float = 0.05,
                 seed: int = 0) -> tuple[float, float]:
    r = rng(seed, "bootstrap"); vals = sorted(stat([r.choice(xs) for _ in xs]) for _ in range(b))
    return vals[int(b * alpha / 2)], vals[int(b * (1 - alpha / 2)) - 1]


def _summarize(runs: list[dict[str, float]]) -> dict[str, object]:
    ret = [x["return"] for x in runs]; cost = [x["cost"] for x in runs]
    return {"iqm": iqm(ret), "ci": bootstrap_ci(ret), "mean_cost": statistics.fmean(cost), "returns": ret}


def evaluate(make_policy: PolicyFactory, seeds: list[int]) -> dict[str, object]:
    return _summarize([run_episode(make_policy, s) for s in seeds])


async def _run_with_retry(make_policy: PolicyFactory, seed: int, sem: asyncio.Semaphore, *, timeout: float,
                          retries: int, base: float, cap: float) -> dict[str, float]:
    for attempt in range(retries + 1):
        try:
            async with sem:
                async with asyncio.timeout(timeout):
                    return await asyncio.to_thread(run_episode, make_policy, seed)
        except TimeoutError:                       # the only error we retry; everything else propagates
            if attempt == retries:
                raise
            delay = random.Random(derive_seed(seed, "retry", attempt)).uniform(0.0, min(cap, base * 2 ** attempt))
            log.warning("seed %d timed out (attempt %d/%d); retrying in %.3fs", seed, attempt + 1, retries + 1, delay)
            await asyncio.sleep(delay)
    raise AssertionError("unreachable")


async def evaluate_async(make_policy: PolicyFactory, seeds: list[int], *, concurrency: int = 4, timeout: float = 60.0,
                         retries: int = 3, base: float = 0.1, cap: float = 2.0) -> dict[str, object]:
    sem = asyncio.Semaphore(concurrency)
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_run_with_retry(make_policy, s, sem, timeout=timeout, retries=retries, base=base, cap=cap))
                 for s in seeds]
    return _summarize([t.result() for t in tasks])