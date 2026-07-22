import math

from codex_behavior_today.metrics import jsd, status_for


def test_jsd_is_symmetric_and_zero_for_equal_distributions():
    left = {"1": 10, "2": 2}
    right = {"1": 2, "2": 10}
    assert jsd(left, left) == 0
    assert math.isclose(jsd(left, right), jsd(right, left))


def test_status_needs_fourteen_prior_days():
    current = {"cells": {"coin": {"counts": {"heads": 10, "tails": 10}}}}
    prior = [{"cells": {"coin": {"counts": {"heads": 10, "tails": 10}}}} for _ in range(13)]
    assert status_for(current, prior) == ("insufficient baseline", None)
