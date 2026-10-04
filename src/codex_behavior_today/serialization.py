from __future__ import annotations

import json
import math


def public_json(value: object) -> str:
    def finite(item: object) -> object:
        if isinstance(item, float) and not math.isfinite(item):
            return None
        if isinstance(item, dict):
            return {key: finite(child) for key, child in item.items()}
        if isinstance(item, list):
            return [finite(child) for child in item]
        return item

    return json.dumps(finite(value), ensure_ascii=False, indent=2, allow_nan=False) + "\n"
