# Temporal Memory Core

**Remembering is easy. Remembering that an old truth can become a current bug is the interesting part.**

This is a public slice of the memory model behind my private Niyam-AI work.

A memory here is not just text. It has two clocks, a use boundary, lifecycle state, and supersession.

![Temporal retrieval workflow](docs/workflow.svg)

## The uncomfortable rule

**Filter first. Rank second.**

A stale or forbidden memory does not get to win because its embedding — or in this tiny public version, its words — happen to match beautifully.

The pipeline asks:

1. did the system know this by the requested knowledge time?
2. was it true at the requested world time?
3. is it allowed for this use?
4. is it still active?
5. has an eligible newer memory superseded it?
6. only then: how relevant is it?

## Why two clocks?

Because these are different questions:

- “When did this become true?”
- “When did the system learn it?”

If a preference changed in March but the assistant only learned that in April, a February reconstruction should not magically know the future.

## Repo map

| Area | Responsibility |
|---|---|
| `models.py` | immutable memory record |
| `time.py` | knowledge-time and valid-time rules |
| `filters.py` | permission, state, and supersession |
| `ranking.py` | small auditable relevance scorer |
| `core.py` | stable public facade |
| `tests/` | time, permission, supersession, ranking |
| `docs/` | the reasoning behind the model |

The private project adds SQLite persistence, audit history, export ingestion, candidate review, evals, and model adapters. None of that personal data belongs here.

Want to inspect the time semantics? Read the [invariants](docs/invariants.md), [failure modes](docs/failure-modes.md), [eligibility table](docs/eligibility-table.md), and [preference-change walkthrough](docs/walkthrough.md).

> Memory should be helpful, not haunted.

## Inspect deeper

- [Design overview](docs/overview.md)
- [Why the design looks this way](docs/decisions.md)
- [Invariants that must survive refactors](docs/invariants.md)
- [How it fails on purpose](docs/failure-modes.md)
- [Security / privacy boundary](SECURITY.md)
- [Where this public slice came from](PROVENANCE.md)

The README is the front door. The interesting arguments are in those files.
