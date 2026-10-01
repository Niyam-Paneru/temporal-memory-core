# Temporal Memory Core

A small Python reference implementation for deciding **which memories are eligible at a requested knowledge time and world time before relevance ranking begins**.

![Temporal memory eligibility decision tree](docs/workflow.svg)

## Eligibility before relevance

`retrieve()` does not score every stored row and hope the best match is safe. It first narrows the candidate set in this order:

1. **Known by `known_at`?** `learned_at <= known_at`; otherwise exclude it as future knowledge.
2. **Valid at `at`?** `at` must be on/after `valid_from` (or `learned_at` when no `valid_from` is set) and before `valid_until` when present.
3. **Allowed for this use?** `required_use` must be in `allowed_use`.
4. **Active?** `status` must equal `"active"`.
5. **Superseded by an eligible row?** Only IDs named by rows that survived the first four gates are removed.
6. **Relevant?** The remaining rows receive a small lexical token-overlap score. Zero-overlap rows are dropped; the rest are ordered by score, then ID, and truncated to `top_k`.

That ordering is the contract: an ineligible row cannot score its way back into a result, and a future or forbidden superseding row cannot erase an older eligible memory.

## Two clocks, one concrete example

Suppose a synthetic record says an office moved on **February 1**, but the system did not learn that fact until **February 10**:

```python
Memory(
    id="office-location",
    text="office is in Patan",
    valid_from="2026-02-01T00:00:00Z",
    learned_at="2026-02-10T00:00:00Z",
)
```

For the same world time, `at=2026-02-05T00:00:00Z`:

- with `known_at=2026-02-20T00:00:00Z`, the record passes both time gates: by February 20 the system knows the move was already true on February 5;
- with `known_at=2026-02-05T00:00:00Z`, it is excluded: a reconstruction of what the system knew on February 5 cannot use knowledge learned five days later.

This is why `at` and `known_at` are separate inputs rather than one generic timestamp.

## Where to inspect the implementation

| File | What it proves |
|---|---|
| [`src/temporal_memory/time.py`](src/temporal_memory/time.py) | UTC parsing, knowledge-time gate, valid-time interval semantics |
| [`src/temporal_memory/filters.py`](src/temporal_memory/filters.py) | permission, lifecycle, and eligible-only supersession |
| [`src/temporal_memory/ranking.py`](src/temporal_memory/ranking.py) | auditable lexical scoring, abstention, deterministic ordering |
| [`src/temporal_memory/models.py`](src/temporal_memory/models.py) | immutable public memory record |
| [`tests/test_core.py`](tests/test_core.py) | end-to-end retrieval contract, including historical supersession |
| [`tests/`](tests/) | focused time, filter, ranking, and facade behavior |

## Run the proof

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

The repository's CI also compiles `src/` and checks the public proof/documentation boundary.

## Scope and provenance

This repository demonstrates temporal eligibility over **synthetic records**. The public implementation uses lexical token overlap for ranking; it does **not** include a personal memory database, ChatGPT export data, persistence layer, embedding/vector database, model adapter, or production access controls.

The privacy boundary is in [`SECURITY.md`](SECURITY.md), and the public/private claim boundary is in [`PROVENANCE.md`](PROVENANCE.md). For the behavioral contract, see [`docs/invariants.md`](docs/invariants.md), [`docs/eligibility-table.md`](docs/eligibility-table.md), and [`docs/failure-modes.md`](docs/failure-modes.md).
