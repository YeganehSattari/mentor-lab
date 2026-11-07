"""Baseline policies for the daily top-K feedback decision. Every select() can also return propensities (for OPE)."""
from __future__ import annotations

import math
import random
from typing import Sequence

from .seeds import rng


class RandomPolicy:
    def __init__(self, seed: int = 0):
        self.r = rng(seed, "random-policy")

    def select(self, contexts: list[list[float]], k: int) -> list[int]:
        return self.r.sample(range(len(contexts)), k)

    def update(self, contexts: list[list[float]], chosen: Sequence[int], rewards: Sequence[float]) -> None:
        return None


class RoundRobin:
    """The 'fair rotation' a busy mentor would do by hand."""
    def __init__(self) -> None:
        self.ptr = 0

    def select(self, contexts: list[list[float]], k: int) -> list[int]:
        n = len(contexts); out = [(self.ptr + j) % n for j in range(k)]; self.ptr = (self.ptr + k) % n
        return out

    def update(self, contexts: list[list[float]], chosen: Sequence[int], rewards: Sequence[float]) -> None:
        return None


class LinUCB:
    """Disjoint-free (shared) LinUCB over intern contexts, top-K by UCB. Reward per chosen intern = active next day.
    A plain-Python implementation (d is small) with Sherman–Morrison updates of A^{-1}."""
    def __init__(self, d: int, alpha: float = 0.8):
        self.d, self.alpha = d, alpha
        self.Ainv = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
        self.b = [0.0] * d

    def _theta(self) -> list[float]:
        return [sum(self.Ainv[i][j] * self.b[j] for j in range(self.d)) for i in range(self.d)]

    def scores(self, contexts: list[list[float]]) -> list[float]:
        th = self._theta(); out = []
        for x in contexts:
            ax = [sum(self.Ainv[i][j] * x[j] for j in range(self.d)) for i in range(self.d)]
            out.append(sum(t * v for t, v in zip(th, x)) + self.alpha * math.sqrt(max(0.0, sum(a * v for a, v in zip(ax, x)))))
        return out

    def select(self, contexts: list[list[float]], k: int) -> list[int]:
        s = self.scores(contexts)
        return sorted(range(len(s)), key=lambda i: -s[i])[:k]

    def update(self, contexts: list[list[float]], chosen: Sequence[int], rewards: Sequence[float]) -> None:
        for i, r in zip(chosen, rewards):
            x = contexts[i]
            ax = [sum(self.Ainv[a][j] * x[j] for j in range(self.d)) for a in range(self.d)]
            den = 1.0 + sum(a * v for a, v in zip(ax, x))
            for a in range(self.d):
                for j in range(self.d):
                    self.Ainv[a][j] -= ax[a] * ax[j] / den
            for j in range(self.d):
                self.b[j] += r * x[j]


def softmax_topk(scores: list[float], k: int, temp: float, r: random.Random) -> tuple[list[int], float]:
    """Sample k without replacement (Plackett–Luce); returns (chosen, probability of that ordered slate). m6: OPE."""
    left = list(range(len(scores))); chosen: list[int] = []; p = 1.0
    for _ in range(k):
        w = [math.exp(scores[i] / temp) for i in left]; z = sum(w)
        u, acc = r.random() * z, 0.0
        for i, wi in zip(left, w):
            acc += wi
            if acc >= u:
                chosen.append(i); p *= wi / z; left.remove(i); break
    return chosen, p
