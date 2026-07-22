# Codex Behavior Today

This public repository monitors whether a fixed Codex endpoint's observed behavior has changed relative to its own history. It is not a model identity verifier or a capability benchmark.

## Structure

- `src/` contains the Python sampler, statistics, SQLite persistence, and static-site generator.
- `data/daily/` contains public aggregate-only daily JSON.
- `runtime/` contains the local SQLite database and logs. Never commit it.
- `site/` is the committed static GitHub Pages artifact.
- `docs/` contains Chinese PRD, RFC, test strategy, and working log.

## Safety

- Never commit OAuth tokens, account IDs, raw responses, private SQLite data, shell history, logs, or machine paths.
- Keep public conclusions narrowly phrased: observed behavior changed, stayed within the observed range, or lacks a sufficient baseline.
- A daily push is externally visible. Only create or alter its schedule with explicit user authorization.

## Development

- Use a project-local `.venv` created with `uv`; install with `uv pip install --python .venv/bin/python -e '.[dev]'`.
- Update `docs/working.md` for meaningful changes.
- Run `python -m pytest -v` and the privacy scan documented in `docs/test.md` before publishing.
- Only commit, push, or create GitHub assets when explicitly requested.
