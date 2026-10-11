from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone

from .models import Memory
from .time import known_by, parse_utc, valid_at


def eligible(
    memory: Memory,
    *,
    at: datetime,
    known_at: datetime,
    required_use: str,
) -> bool:
    if not known_by(memory.learned_at, known_at=known_at):
        return False
    if not valid_at(
        learned_at=memory.learned_at,
        valid_from=memory.valid_from,
        valid_until=memory.valid_until,
        at=at,
    ):
        return False
    if required_use not in memory.allowed_use:
        return False
    if memory.status != "active":
        return False
    return True


def active_memories(
    memories: Iterable[Memory],
    *,
    at: datetime | None = None,
    known_at: datetime | None = None,
    required_use: str = "retrieval",
) -> list[Memory]:
    now = datetime.now(timezone.utc)
    at = at or now
    known_at = known_at or now

    eligible_rows = [
        memory
        for memory in memories
        if eligible(memory, at=at, known_at=known_at, required_use=required_use)
    ]

    # Supersession cannot erase a peer, a newer fact, or the source itself.
    # Compare knowledge time: a later-learned correction may be backdated in world time.
    learned_at_by_id = {memory.id: parse_utc(memory.learned_at) for memory in eligible_rows}
    superseded_ids: set[str] = set()
    for replacement in eligible_rows:
        replacement_learned_at = parse_utc(replacement.learned_at)
        if replacement_learned_at is None:
            continue
        for previous_id in replacement.supersedes:
            previous_learned_at = learned_at_by_id.get(previous_id)
            if previous_learned_at is not None and replacement_learned_at > previous_learned_at:
                superseded_ids.add(previous_id)

    return [memory for memory in eligible_rows if memory.id not in superseded_ids]
