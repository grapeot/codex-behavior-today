# Codex Behavior Today

Codex Behavior Today is a small public dashboard answering one narrow question: under a fixed set of short prompts, does today's observed Codex endpoint behavior remain within its own historical range?

It does not identify model weights, prove model substitution, or measure general model capability. A notable shift means only that this endpoint's sampled answer distribution changed enough to merit a closer look.

## How It Works

Each daily run collects 100 short answers across five fixed prompt cells. The local runner retains raw answers in a private SQLite database, then publishes only aggregate counts, latency summaries, and distribution-distance metrics. The committed `site/` directory is deployed as GitHub Pages.

## Local Setup

Create a virtual environment, then install the package:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e '.[dev]'
```

The sampler delegates authenticated requests to a locally installed ChatGPT/Codex OAuth compatibility CLI. Set its absolute path locally:

```bash
export CODEX_BEHAVIOR_OAUTH_CLI=/path/to/chatgpt-oauth
export CODEX_BEHAVIOR_MODEL=gpt-5.6-sol
```

Run one daily sample and build the site:

```bash
.venv/bin/python -m codex_behavior_today run
```

Build the static site from existing public aggregates only:

```bash
.venv/bin/python -m codex_behavior_today build-site
```

## Privacy

Credentials and raw answers stay local. The public repository contains aggregate daily JSON only. The local SQLite database defaults to `runtime/behavior.sqlite3` and is excluded from Git.

## License

MIT
