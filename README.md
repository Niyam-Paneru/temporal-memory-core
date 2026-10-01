# Temporal Memory Core

**Remembering is easy. Remembering that an old truth can become a current bug is the interesting part.**

This repo is a public, sanitized slice of the memory model behind my private `Niyam-AI` work.

A memory here is not just text. It carries:

- when it was learned;
- when it was valid;
- what it supersedes;
- what it is allowed to be used for;
- whether it is active, uncertain, or retired.

## The rule

```text
retrieve candidate
        |
        v
known by then? ---- no ---> exclude
        |
       yes
        |
        v
valid at that time? -- no --> exclude
        |
       yes
        |
        v
allowed for this use? -- no --> exclude
        |
       yes
        |
        v
superseded by an eligible newer memory? -- yes --> exclude
        |
       no
        |
        v
rank
```

If retrieval is allowed to “sort first, filter later,” stale personal facts can win simply because they match the query well. That is exactly backwards.

## Run

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Example

```python
from datetime import datetime, timezone
from temporal_memory.core import Memory, retrieve

memories = [
    Memory(
        id="old",
        text="prefers long answers",
        learned_at="2026-01-01T00:00:00Z",
        valid_from="2026-01-01T00:00:00Z",
        valid_until="2026-03-01T00:00:00Z",
        allowed_use=frozenset({"retrieval"}),
    ),
    Memory(
        id="new",
        text="prefers concise answers",
        learned_at="2026-03-01T00:00:00Z",
        valid_from="2026-03-01T00:00:00Z",
        supersedes=("old",),
        allowed_use=frozenset({"retrieval"}),
    ),
]

print(retrieve("answer preference", memories))
```

## What this proves

- valid-time vs knowledge-time filtering;
- supersession;
- permission-before-ranking;
- deterministic lexical retrieval;
- deliberate abstention when nothing eligible exists.

## Boundary

No ChatGPT export, private conversation text, embeddings, API keys, personal database, or user data is included here.

## Provenance

Rewritten from the memory/retrieval experiments in private `Niyam-AI`. The private project contains a larger SQLite store, audit log, candidate-review pipeline, eval harness, continuity ledger, and model adapters.
