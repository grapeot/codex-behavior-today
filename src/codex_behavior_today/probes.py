from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Probe:
    slug: str
    prompt: str
    kind: str


PROBE_BATTERY_VERSION = "v1"

PROBES = (
    Probe("number_1_10", "Reply with exactly one random integer from 1 through 10. Output only the integer.", "number_1_10"),
    Probe("coin_flip", "Reply with exactly one random coin-flip result: heads or tails. Output only heads or tails.", "coin_flip"),
    Probe("letter", "Reply with exactly one random English letter from A through Z. Output only the letter.", "letter"),
    Probe("number_1_100", "Reply with exactly one random integer from 1 through 100. Output only the integer.", "number_1_100"),
    Probe("favorite_number", "Reply with exactly one integer: your favorite number. Output only the integer.", "favorite_number"),
)
