# Walkthrough: a preference changes

Imagine two records:

- January: “prefers long answers”
- March: “prefers concise answers”, superseding the January record

Now ask three different questions.

## What was known in February?

The March record did not exist yet, so it cannot suppress January.

Result: **prefers long answers**.

## What is valid in April?

The March record is known, valid, active, and supersedes January.

Result: **prefers concise answers**.

## What if the March record is not allowed for this use?

It fails eligibility before supersession and before ranking.

The January record is not automatically erased merely because a forbidden newer row exists.

This is why “latest row wins” is too weak for personal memory. Time and permission are part of retrieval semantics, not metadata decoration.
