# Working Log

## Changelog

### 2026-07-22

- Created the public-project scaffold, privacy boundary, measurement contract, and GitHub Pages deployment design.
- Implemented the local sampler, aggregate-only export, static Pages artifact, and offline tests.
- Collected the first 100-sample baseline through the Codex subscription compatibility transport.

## Lessons Learned

- The dashboard monitors a subscription endpoint behavior envelope, not a model identity.
- Raw responses are needed for local audit but must never enter the public aggregate history.
