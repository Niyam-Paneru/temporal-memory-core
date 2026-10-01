from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
import re

from .filters import active_memories
from .models import Memory


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def lexical_score(query: str, memory: Memory) -> int:
    return len(tokens(query) & tokens(memory.text))


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

    rows = active_memories(
        memories,
        at=at,
        known_at=known_at,
        required_use=required_use,
    )

    scored = [
        (lexical_score(query, memory), memory.id, memory)
        for memory in rows
    ]
    scored = [row for row in scored if row[0] > 0]
    scored.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in scored[:top_k]]
