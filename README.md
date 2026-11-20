# Temporal Memory Core

An office moves on **February 1**. The assistant only learns about it on **February 10**. Ask what it knew on February 5, and it confidently gives the new address.

I've apparently built a time machine. Terrible feature for a memory system.

This Python module keeps two dates for a fact: **when it was true**, and **when the assistant learned it**. They aren't interchangeable.

## Time travel, but with paperwork

| Question | Valid date | Knowledge cutoff | Result |
| --- | --- | --- | --- |
| “What could we say on February 5?” | Feb 5 | Feb 5 | Exclude the move; we hadn't learned it |
| “Knowing what we know now, what was true on February 5?” | Feb 5 | Feb 20 | The move can be included; we learned it Feb 10 |
| “What if no eligible fact matches?” | Any | Any | No invented memory; return no match |

**Valid time** tells us when the fact was true. **Knowledge time** tells us when the system learned it. A historical answer needs both.

## The boring checks that prevent magical knowledge

Retrieval filters by allowed use, valid-time bounds, knowledge-time bounds, and active status **before** ranking. Only eligible newer memories can supersede older eligible ones. The public ranking uses lexical overlap, not a hidden LLM.

Relevant source: [time logic](src/temporal_memory/time.py), [filters and supersession](src/temporal_memory/filters.py), [ranking](src/temporal_memory/ranking.py), and [tests](tests/). For precise cases, use the [eligibility table](docs/eligibility-table.md) and [verification](docs/verification.md).

This is a **synthetic-memory rule engine**. It does not include a personal memory dump, vector index, persistence service, real user authentication, or a deployed AI assistant.

If the assistant knows tomorrow's news yesterday, I'd like to borrow it for the lottery. Until then, the timestamps stay separate.
