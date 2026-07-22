from codex_behavior_today.normalize import canonicalize


def test_canonicalize_closed_answer_spaces():
    assert canonicalize("number_1_10", " 07. ") == "7"
    assert canonicalize("coin_flip", "Heads") == "heads"
    assert canonicalize("letter", "Q") == "q"
    assert canonicalize("number_1_100", "101") is None
    assert canonicalize("coin_flip", "a coin") is None
