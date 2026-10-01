# Design overview

A personal-memory system has at least two clocks:

- **knowledge time** — when the system learned the record;
- **valid time** — when the record was true.

Those clocks are not interchangeable.

A fact learned in April should not appear in a reconstruction of what was known in February. A preference that stopped being true in March should not win today's retrieval just because its wording matches perfectly.

The public module therefore filters **before** it ranks:

1. was this known by the requested knowledge time?
2. was it valid at the requested world time?
3. is it allowed for this use?
4. is it active?
5. has an eligible newer record superseded it?
6. only then: score relevance.

The private Niyam-AI project adds persistence, audit history, candidate review, export ingestion, and evaluation. This repo isolates the temporal contract.
