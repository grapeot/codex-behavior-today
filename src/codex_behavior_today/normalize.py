from __future__ import annotations

import re


def canonicalize(kind: str, raw: str) -> str | None:
    text = raw.strip().lower().strip("`'\".!,;:()[]{}")
    if kind == "coin_flip":
        return text if text in {"heads", "tails"} else None
    if kind == "letter":
        return text if re.fullmatch(r"[a-z]", text) else None
    if kind == "number_1_10":
        return _bounded_integer(text, 1, 10)
    if kind == "number_1_100":
        return _bounded_integer(text, 1, 100)
    if kind == "favorite_number":
        return str(int(text)) if re.fullmatch(r"-?\d{1,6}", text) else None
    raise ValueError(f"Unknown probe kind: {kind}")


def _bounded_integer(text: str, low: int, high: int) -> str | None:
    if not re.fullmatch(r"\d{1,3}", text):
        return None
    value = int(text)
    return str(value) if low <= value <= high else None
