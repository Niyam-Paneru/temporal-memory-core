from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Iterable


def _dt(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


@dataclass(frozen=True)
class Memory:
    id: str
    text: str
    learned_at: str
    valid_from: str | None = None
    valid_until: str | None = None
    supersedes: tuple[str, ...] = ()
    allowed_use: frozenset[str] = field(default_factory=lambda: frozenset({"retrieval"}))
    status: str = "active"


def eligible(
    memory: Memory,
    *,
    at: datetime,
    known_at: datetime,
    required_use: str,
) -> bool:
    learned = _dt(memory.learned_at)
    valid_from = _dt(memory.valid_from) or learned
    valid_until = _dt(memory.valid_until)

    if learned is None or learned > known_at:
        return False
    if valid_from is not None and at < valid_from:
        return False
    if valid_until is not None and at >= valid_until:
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
        m for m in memories
        if eligible(m, at=at, known_at=known_at, required_use=required_use)
    ]

    superseded = {
        old_id
        for memory in eligible_rows
        for old_id in memory.supersedes
    }

    return [m for m in eligible_rows if m.id not in superseded]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(
    query: str,
    memories: Iterable[Memory],
    *,
    top_k: int = 5,
    at: datetime | None = None,
    known_at: datetime | None = None,
    required_use: str = "retrieval",
) -> list[Memory]:
    if top_k < 1:
        return []

    query_tokens = _tokens(query)
    rows = active_memories(
        memories,
        at=at,
        known_at=known_at,
        required_use=required_use,
    )

    scored: list[tuple[int, str, Memory]] = []
    for memory in rows:
        overlap = len(query_tokens & _tokens(memory.text))
        if overlap > 0:
            scored.append((overlap, memory.id, memory))

    scored.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in scored[:top_k]]
