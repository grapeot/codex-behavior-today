import json
import math
import re
import shutil
import subprocess

import pytest

from codex_behavior_today import DEFAULT_MODEL
from codex_behavior_today.site import build_site


def day(model, date="2026-01-01"):
    return {
        "date": date,
        "measurement": {"model": model},
        "total_valid": 20,
        "total_attempts": 20,
        "total_invalid": 0,
        "cells": {"coin_flip": {"counts": {"heads": 10, "tails": 10}, "valid": 20, "attempts": 20}},
        "metrics": {"baseline_jsd": math.nan, "status": "insufficient baseline"},
    }


@pytest.mark.parametrize(
    "models,show_warning",
    [
        (["gpt-5.6-sol"], True),
        (["gpt-5.6-sol", DEFAULT_MODEL], True),
        ([DEFAULT_MODEL], False),
        (["gpt-5.6-sol"] + [DEFAULT_MODEL] * 30, False),
    ],
)
def test_dashboard_warns_only_for_visible_cross_model_history(tmp_path, models, show_warning):
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node is required to execute dashboard JavaScript")
    days = [day(model, f"2026-01-{index + 1:02}") for index, model in enumerate(models)]
    build_site(days, tmp_path)
    html = (tmp_path / "index.html").read_text()
    script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    history = (tmp_path / "data" / "history.json").read_text()
    program = r"""
const fs=require('fs'),vm=require('vm');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const elements={};
const document={querySelector:key=>elements[key]??=( {innerHTML:'',hidden:true} ),querySelectorAll:()=>[]};
vm.runInNewContext(input.script,{document,fetch:()=>Promise.resolve({json:()=>Promise.resolve(JSON.parse(input.history))})});
setImmediate(()=>console.log(JSON.stringify(elements)));
"""
    result = subprocess.run(
        [node, "-e", program],
        input=json.dumps({"script": script, "history": history}),
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    elements = json.loads(result.stdout)
    assert elements["#model-warning"]["hidden"] is not show_warning
    if show_warning:
        assert "not directly comparable" in elements["#model-warning"]["innerHTML"]
        assert "gpt-5.6-sol" in elements["#model-warning"]["innerHTML"]
        assert DEFAULT_MODEL in elements["#model-warning"]["innerHTML"]
    assert models[-1] in elements["#selected-note"]["innerHTML"]
    assert models[-1] in elements["#summary"]["innerHTML"]
    assert "Public data could not be loaded" not in elements["#summary"]["innerHTML"]


def test_site_serializes_unavailable_metrics_without_changing_source(tmp_path):
    source = day("gpt-5.6-sol")
    source["metrics"]["other"] = [math.inf, -math.inf, 0.0]
    build_site([source], tmp_path)
    history = (tmp_path / "data" / "history.json").read_text()
    assert "NaN" not in history and "Infinity" not in history
    assert json.loads(history)[0]["metrics"] == {
        "baseline_jsd": None,
        "status": "insufficient baseline",
        "other": [None, None, 0.0],
    }
    assert math.isnan(source["metrics"]["baseline_jsd"])
