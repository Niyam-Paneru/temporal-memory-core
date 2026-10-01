import unittest
from datetime import datetime, timezone

from temporal_memory.filters import active_memories
from temporal_memory.models import Memory


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class FilterTests(unittest.TestCase):
    def test_use_permission_is_checked_before_ranking(self):
        memory = Memory(
            id="m",
            text="concise answer preference",
            learned_at="2026-01-01T00:00:00Z",
            allowed_use=frozenset({"evaluation"}),
        )
        self.assertEqual(active_memories([memory], required_use="retrieval"), [])

    def test_retired_memory_is_not_active(self):
        memory = Memory(
            id="m",
            text="old fact",
            learned_at="2026-01-01T00:00:00Z",
            status="retired",
        )
        self.assertEqual(active_memories([memory]), [])

    def test_eligible_new_memory_supersedes_old(self):
        old = Memory(id="old", text="prefers long answers", learned_at="2026-01-01T00:00:00Z")
        new = Memory(
            id="new",
            text="prefers concise answers",
            learned_at="2026-03-01T00:00:00Z",
            supersedes=("old",),
        )
        ids = [m.id for m in active_memories([old, new], known_at=dt("2026-04-01T00:00:00Z"))]
        self.assertEqual(ids, ["new"])

    def test_future_superseding_memory_does_not_erase_past(self):
        old = Memory(id="old", text="prefers long answers", learned_at="2026-01-01T00:00:00Z")
        new = Memory(
            id="new",
            text="prefers concise answers",
            learned_at="2026-03-01T00:00:00Z",
            supersedes=("old",),
        )
        ids = [m.id for m in active_memories([old, new], known_at=dt("2026-02-01T00:00:00Z"))]
        self.assertEqual(ids, ["old"])


if __name__ == "__main__":
    unittest.main()
