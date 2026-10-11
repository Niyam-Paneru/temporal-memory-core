# Verification

Run from the repository root with Python 3.10+.

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

The behavior suite checks the two-clock model, use permissions, lifecycle filtering, eligible-only supersession, lexical ranking, deterministic ordering, and abstention when no eligible relevant memory remains.

CircleCI additionally compiles `src/` and verifies that the public documentation and provenance files are present.

Malformed timestamps in stored records (learned time, valid start, valid end)
exclude **only that record**. They must not abort retrieval, become an open-ended
interval, or supersede healthy memories. Invalid caller-provided query clocks
still raise `ValueError` rather than being silently treated as absent.

See `tests/test_invalid_time_records.py` for these failure-path checks.
