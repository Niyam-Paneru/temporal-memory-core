# Failure modes

## Future knowledge leaks into the past
A fact learned later appears in an earlier reconstruction. Response: enforce knowledge-time filtering before ranking.

## Stale truth wins on similarity
An old preference matches the query strongly. Response: valid-time filtering happens before relevance scoring.

## Forbidden memory is highly relevant
A memory is not allowed for retrieval but matches perfectly. Response: exclude it before ranking.

## Future supersession rewrites history
A newer record hides an older record at a time when the newer record was not yet known. Response: only eligible superseding records can suppress older ones.

## Stale or self-referential supersession erases valid memory
An older eligible row names a newer row in `supersedes`, or a row names itself. Response: require a strictly later `learned_at` instant for the superseding row, independent of backdated world validity.

## No eligible result
Everything is stale, forbidden, retired, or irrelevant. Response: abstain.

## Retired record reappears
A retired record is still present in storage. Response: lifecycle status participates in eligibility.
