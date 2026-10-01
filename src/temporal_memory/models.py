from __future__ import annotations

from dataclasses import dataclass, field


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
