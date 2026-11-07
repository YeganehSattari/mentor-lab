"""Independent, order-proof random streams: never rely on random's global state or on hash()."""
import hashlib
import random


def derive_seed(base: int, *keys: object) -> int:
    """Stable 64-bit seed from a base seed and any labels (independent of PYTHONHASHSEED)."""
    h = hashlib.sha256(repr((base,) + keys).encode()).digest()
    return int.from_bytes(h[:8], "big")


def rng(base: int, *keys: object) -> random.Random:
    return random.Random(derive_seed(base, *keys))
