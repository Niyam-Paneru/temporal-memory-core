# Decisions

## Two clocks, not one timestamp

`learned_at` answers “when did the system know this?” while `valid_from` / `valid_until` answer “when was this true?”

Collapsing them creates historical leakage.

## Permission before similarity

A memory that is not allowed for retrieval never reaches the ranker. A very relevant forbidden memory is still forbidden.

## Supersession is conditional on eligibility

A newer record only hides an older one when the newer record itself is eligible at the requested time. Otherwise future knowledge would rewrite the past.

## Abstention is normal

No lexical overlap returns no result. Retrieval is not required to manufacture a candidate just so the UI has something to show.

> Memory should be helpful, not haunted.
