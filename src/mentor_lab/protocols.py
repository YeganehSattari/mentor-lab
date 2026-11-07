from __future__ import annotations
from typing import Protocol, Sequence, TypeVar

S = TypeVar("S"); A = TypeVar("A")
S_co = TypeVar("S_co", covariant=True)
S_contra = TypeVar("S_contra", contravariant=True)
A_contra = TypeVar("A_contra", contravariant=True)

Context = list[list[float]]

class Env(Protocol[S_co, A_contra]):
    def reset(self, seed: int) -> S_co: ...
    def step(self, chosen: Sequence[A_contra]) -> tuple[S_co, float, float, bool]: ...

class Policy(Protocol[S_contra, A]):
    def select(self, contexts: S_contra, k: int) -> list[A]: ...
    def update(self, contexts: S_contra, chosen: Sequence[A], rewards: Sequence[float]) -> None: ...