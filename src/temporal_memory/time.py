from __future__ import annotations

from datetime import datetime, timezone


def parse_utc(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def require_aware(value: datetime, *, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name}_must_be_timezone_aware")
    return value.astimezone(timezone.utc)


def known_by(learned_at: str, *, known_at: datetime) -> bool:
    # Invalid query clocks are caller errors, even if the record itself is bad.
    known_at = require_aware(known_at, name="known_at")
    try:
        learned = parse_utc(learned_at)
    except (TypeError, ValueError, AttributeError, OverflowError):
        return False  # invalid evidence never becomes eligible
    return learned is not None and learned <= known_at


def valid_at(
    *,
    learned_at: str,
    valid_from: str | None,
    valid_until: str | None,
    at: datetime,
) -> bool:
    at = require_aware(at, name="at")
    try:
        learned = parse_utc(learned_at)
        start = parse_utc(valid_from) or learned
        end = parse_utc(valid_until)
    except (TypeError, ValueError, AttributeError, OverflowError):
        # In particular, a malformed valid_until must not be mistaken for
        # an absent end date (which would make a memory valid forever).
        return False

    if start is None or at < start:
        return False
    if end is not None and at >= end:
        return False
    return True
