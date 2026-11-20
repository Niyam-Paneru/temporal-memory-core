# Temporal Memory Core

An office moves on **February 1**. The assistant learns about the move on **February 10**.

Ask what it knew on February 5. If it gives you the new address, congratulations: you've built a time machine, and unfortunately it only works for incorrect answers.

This Python module separates **when a fact was true** from **when the assistant learned it**.

## Two clocks; one inconvenient calendar

| Question | Valid date | Knowledge cutoff | Result |
| --- | --- | --- | --- |
| “What could we say on February 5?” | Feb 5 | Feb 5 | Exclude the move; we hadn't learned it |
| “Knowing what we know now, what was true on February 5?” | Feb 5 | Feb 20 | The move can be included; we learned it Feb 10 |
| “What if no eligible fact matches?” | Any | Any | No invented memory; return no match |

The distinction is between **valid time** and **knowledge time**. They answer different questions; squashing them into one timestamp doesn't make them agree.

## Permission before cleverness

Retrieval filters by allowed use, valid-time bounds, knowledge-time bounds, and active status **before** ranking. Only eligible newer memories can supersede older eligible ones. The public ranking is lexical overlap, not a hidden LLM performing dramatic deductions under the floorboards.

Relevant source: [time logic](src/temporal_memory/time.py), [filters and supersession](src/temporal_memory/filters.py), [ranking](src/temporal_memory/ranking.py), and [tests](tests/). For precise cases, use the [eligibility table](docs/eligibility-table.md) and [verification](docs/verification.md).

This is a **synthetic-memory rule engine**. It does not include a personal memory dump, vector index, persistence service, real user authentication, or a deployed AI assistant.

The point isn't to remember everything. It's to remember what you were actually allowed to know **at the time**, which turns out to be the harder part.
