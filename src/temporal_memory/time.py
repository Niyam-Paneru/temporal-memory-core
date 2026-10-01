from __future__ import annotations

from datetime import datetime, timezone


def parse_utc(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def known_by(learned_at: str, *, known_at: datetime) -> bool:
    learned = parse_utc(learned_at)
    return learned is not None and learned <= known_at


def valid_at(
    *,
    learned_at: str,
    valid_from: str | None,
    valid_until: str | None,
    at: datetime,
) -> bool:
    learned = parse_utc(learned_at)
    start = parse_utc(valid_from) or learned
    end = parse_utc(valid_until)

    if start is None or at < start:
        return False
    if end is not None and at >= end:
        return False
    return True
