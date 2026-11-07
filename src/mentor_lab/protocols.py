"""Minimal typed contracts. m1 task: make these Generic Protocols pass mypy/pyright --strict."""
from __future__ import annotations

from typing import Protocol, Sequence


class Env(Protocol):
    def reset(self, seed: int) -> list[list[float]]: ...
    def step(self, chosen: Sequence[int]) -> tuple[list[list[float]], float, float, bool]: ...


class Policy(Protocol):
    def select(self, contexts: list[list[float]], k: int) -> list[int]: ...
    def update(self, contexts: list[list[float]], chosen: Sequence[int], rewards: Sequence[float]) -> None: ...
