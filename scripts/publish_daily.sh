#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h:h}"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

./.venv/bin/python -m pytest -v
PATTERN='/U''sers/|op:''//|access''_token|refresh''_token|account''_id|BE''GIN .*PRIVATE'
rg -n "$PATTERN" . --glob '!runtime/**' --glob '!*.lock' --glob '!.env' && exit 1 || true

if [[ "${1:-}" == "--check" ]]; then
  exit 0
fi

./.venv/bin/python -m codex_behavior_today run
git add data/daily site docs/working.md
git diff --cached --quiet || git commit -m "data: update daily Codex behavior"
git push origin master
