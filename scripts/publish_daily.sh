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

git fetch origin master
git checkout master
git pull --ff-only origin master
RUN_DATE="$(date +%F)"
BRANCH="data/codex-behavior-${RUN_DATE}"
git checkout -B "$BRANCH" origin/master

./.venv/bin/python -m codex_behavior_today run
git add data/daily site
if git diff --cached --quiet; then
  git checkout master
  exit 0
fi
git commit -m "data: update daily Codex behavior"
git push --set-upstream origin "$BRANCH"
PR_URL="$(gh pr create --base master --head "$BRANCH" --title "data: update daily Codex behavior" --body "Automated aggregate-only daily endpoint behavior update.")"
gh pr merge "$PR_URL" --merge --delete-branch
git checkout master
git pull --ff-only origin master
