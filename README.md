# Temporal Memory Core

The office moves on **February 1**. Nobody tells the assistant until **February 10**.

Ask what it knew on February 5. If it confidently gives you the new address, it has either mastered time travel or quietly cheated on the timeline. I'm not betting on time travel.

This Python module keeps **when a fact was true** separate from **when the assistant learned it**.

## Two clocks, one event

| Question | Valid date | Knowledge cutoff | Result |
| --- | --- | --- | --- |
| “What could we say on February 5?” | Feb 5 | Feb 5 | Exclude the move; we hadn't learned it |
| “Knowing what we know now, what was true on February 5?” | Feb 5 | Feb 20 | The move can be included; we learned it Feb 10 |
| “What if no eligible fact matches?” | Any | Any | No invented memory; return no match |

**Valid time** tells us when the fact was true. **Knowledge time** tells us when the system learned it. A historical answer needs both.

## First check the calendar. Then the permission.

Retrieval filters by allowed use, valid-time bounds, knowledge-time bounds, and active status **before** ranking. Only eligible newer memories can supersede older eligible ones. The public ranking uses lexical overlap, not a hidden LLM.

Relevant source: [time logic](src/temporal_memory/time.py), [filters and supersession](src/temporal_memory/filters.py), [ranking](src/temporal_memory/ranking.py), and [tests](tests/). For precise cases, use the [eligibility table](docs/eligibility-table.md) and [verification](docs/verification.md).

This is a **synthetic-memory rule engine**. It does not include a personal memory dump, vector index, persistence service, real user authentication, or a deployed AI assistant.

Remembering a fact is easy. Remembering whether you were even supposed to know it yet is where the trouble starts.
