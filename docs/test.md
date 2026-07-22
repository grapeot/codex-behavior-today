# Test Strategy

## Offline Unit Tests

- Canonicalization maps valid answers and rejects invalid output deterministically.
- Jensen-Shannon divergence is symmetric and zero for equal distributions.
- Status logic remains `insufficient baseline` before 14 previous days.
- Static history rendering reads aggregate-only fixtures.

## Live Validation

Live sampling is opt-in. Before a scheduled run, verify the OAuth CLI status, run one sample per cell, then run a complete day manually. Inspect the ignored SQLite database locally and inspect the generated public JSON before any commit.

## Public Hygiene

Before publication run the privacy scan built into `scripts/publish_daily.sh`. It rejects local machine paths, credential field names, vault references, and private-key markers outside ignored local files.

```bash
scripts/publish_daily.sh
```

The command must have no matches in tracked public files.
