# Test Strategy

## Offline Unit Tests

- Canonicalization maps valid answers and rejects invalid output deterministically.
- Jensen-Shannon divergence is symmetric and zero for equal distributions.
- Status logic remains `insufficient baseline` before 14 previous days.
- Static history rendering reads aggregate-only fixtures.
- Execute dashboard JavaScript against mixed-model and pre-transition history to verify the warning renders; target-only visible windows hide it, including after older models roll out of the 30-day view.
- Verify selected-day and latest-run model labels and strict JSON parsing of generated history containing unavailable metrics. Nonfinite values become `null` without changing source aggregates.

## Live Validation

Live sampling is opt-in. Before a scheduled run, verify the OAuth CLI status, run one sample per cell, then run a complete day manually. Inspect the ignored SQLite database locally and inspect the generated public JSON before any commit.

## Public Hygiene

Before publication run the privacy scan built into `scripts/publish_daily.sh`. It rejects local machine paths, credential field names, vault references, and private-key markers outside ignored local files.

```bash
scripts/publish_daily.sh
```

The command must have no matches in tracked public files.
