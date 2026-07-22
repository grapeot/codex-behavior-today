from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping


def jsd(left: Mapping[str, int], right: Mapping[str, int]) -> float:
    left_total = sum(left.values())
    right_total = sum(right.values())
    if not left_total or not right_total:
        return math.nan
    keys = set(left) | set(right)
    divergence = 0.0
    for key in keys:
        p = left.get(key, 0) / left_total
        q = right.get(key, 0) / right_total
        midpoint = (p + q) / 2
        if p:
            divergence += p * math.log2(p / midpoint) / 2
        if q:
            divergence += q * math.log2(q / midpoint) / 2
    return divergence


def aggregate_counts(days: list[dict], slug: str) -> Counter[str]:
    aggregate: Counter[str] = Counter()
    for day in days:
        cell = day.get("cells", {}).get(slug, {})
        aggregate.update(cell.get("counts", {}))
    return aggregate


def weighted_drift(current: dict, reference_days: list[dict]) -> tuple[float, dict[str, float]]:
    scores: dict[str, float] = {}
    weighted_sum = 0.0
    total_weight = 0
    for slug, cell in current.get("cells", {}).items():
        baseline = aggregate_counts(reference_days, slug)
        score = jsd(cell.get("counts", {}), baseline)
        if math.isnan(score):
            continue
        weight = sum(cell.get("counts", {}).values())
        scores[slug] = score
        weighted_sum += score * weight
        total_weight += weight
    return (weighted_sum / total_weight if total_weight else math.nan, scores)


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(value for value in values if not math.isnan(value))
    if not ordered:
        return math.nan
    index = min(len(ordered) - 1, math.ceil(fraction * len(ordered)) - 1)
    return ordered[index]


def status_for(current: dict, prior_days: list[dict]) -> tuple[str, float | None]:
    if len(prior_days) < 14:
        return "insufficient baseline", None
    window = prior_days[-14:]
    drift, _ = weighted_drift(current, window)
    historical: list[float] = []
    for index in range(14, len(prior_days)):
        score, _ = weighted_drift(prior_days[index], prior_days[index - 14:index])
        historical.append(score)
    if not historical:
        return "within observed range", None
    threshold = percentile(historical, 0.99)
    return ("notable shift" if drift > threshold else "within observed range"), threshold
