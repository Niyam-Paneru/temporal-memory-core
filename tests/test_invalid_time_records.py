"""Malformed stored timestamps must not poison retrieval or escape filtering."""

import unittest
from datetime import datetime, timezone

from temporal_memory import Memory, retrieve
from temporal_memory.time import known_by, valid_at


NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)


class MalformedStoredTimeTests(unittest.TestCase):
    def test_corrupt_learned_time_is_excluded_without_crashing_other_records(self):
        healthy = Memory("healthy", "answer preference concise", "2026-01-01T00:00:00Z")
        broken = Memory("broken", "answer preference long", "not-a-time")
        found = retrieve("answer preference", [broken, healthy], at=NOW, known_at=NOW)
        self.assertEqual([m.id for m in found], ["healthy"])

    def test_corrupt_end_date_is_not_interpreted_as_open_ended(self):
        self.assertFalse(valid_at(
            learned_at="2026-01-01T00:00:00Z",
            valid_from=None,
            valid_until="not-a-time",
            at=NOW,
        ))

    def test_corrupt_start_date_is_not_ignored(self):
        self.assertFalse(valid_at(
            learned_at="2026-01-01T00:00:00Z",
            valid_from="2026-02-31T00:00:00Z",
            valid_until=None,
            at=NOW,
        ))

    def test_invalid_superseding_record_cannot_hide_healthy_memory(self):
        old = Memory("old", "answer preference long", "2026-01-01T00:00:00Z")
        corrupt_new = Memory(
            "new",
            "answer preference concise",
            "2026-05-01T00:00:00Z",
            valid_until="unparseable",
            supersedes=("old",),
        )
        found = retrieve("answer preference", [old, corrupt_new], at=NOW, known_at=NOW)
        self.assertEqual([m.id for m in found], ["old"])

    def test_malformed_type_cannot_become_eligible(self):
        self.assertFalse(known_by(123, known_at=NOW))  # type: ignore[arg-type]
        self.assertFalse(valid_at(
            learned_at="2026-01-01T00:00:00Z",
            valid_from=None,
            valid_until=123,  # type: ignore[arg-type]
            at=NOW,
        ))

    def test_invalid_query_clock_is_still_an_explicit_error(self):
        with self.assertRaisesRegex(ValueError, "known_at_must_be_timezone_aware"):
            known_by("not-a-time", known_at=datetime(2026, 6, 1))
        with self.assertRaisesRegex(ValueError, "at_must_be_timezone_aware"):
            valid_at(
                learned_at="not-a-time",
                valid_from=None,
                valid_until=None,
                at=datetime(2026, 6, 1),
            )


if __name__ == "__main__":
    unittest.main()
