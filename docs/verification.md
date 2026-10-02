# Verification

Run from the repository root with Python 3.10+.

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

The behavior suite checks the two-clock model, use permissions, lifecycle filtering, eligible-only supersession, lexical ranking, deterministic ordering, and abstention when no eligible relevant memory remains.

CircleCI additionally compiles `src/` and verifies that the public documentation and provenance files are present.
