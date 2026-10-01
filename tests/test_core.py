import unittest
from datetime import datetime, timezone

from temporal_memory.core import Memory, active_memories, retrieve


def dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class TemporalMemoryTests(unittest.TestCase):
    def test_future_knowledge_is_not_available(self):
        memory = Memory(id="m", text="prefers concise answers", learned_at="2026-04-01T00:00:00Z")
        rows = active_memories([memory], known_at=dt("2026-03-01T00:00:00Z"))
        self.assertEqual(rows, [])

    def test_valid_from_is_respected(self):
        memory = Memory(
            id="m",
            text="new preference",
            learned_at="2026-01-01T00:00:00Z",
            valid_from="2026-05-01T00:00:00Z",
        )
        self.assertEqual(active_memories([memory], at=dt("2026-04-01T00:00:00Z")), [])

    def test_valid_until_is_exclusive(self):
        memory = Memory(
            id="m",
            text="old preference",
            learned_at="2026-01-01T00:00:00Z",
            valid_until="2026-03-01T00:00:00Z",
        )
        self.assertEqual(active_memories([memory], at=dt("2026-03-01T00:00:00Z")), [])

    def test_permission_is_pre_ranking(self):
        hidden = Memory(
            id="hidden",
            text="concise answer preference",
            learned_at="2026-01-01T00:00:00Z",
            allowed_use=frozenset({"evaluation"}),
        )
        self.assertEqual(retrieve("concise answer", [hidden], required_use="retrieval"), [])

    def test_retired_memory_is_excluded(self):
        memory = Memory(
            id="m",
            text="some fact",
            learned_at="2026-01-01T00:00:00Z",
            status="retired",
        )
        self.assertEqual(active_memories([memory]), [])

    def test_eligible_new_memory_supersedes_old(self):
        old = Memory(id="old", text="answer preference long", learned_at="2026-01-01T00:00:00Z")
        new = Memory(
            id="new",
            text="answer preference concise",
            learned_at="2026-03-01T00:00:00Z",
            supersedes=("old",),
        )
        ids = [m.id for m in active_memories([old, new], known_at=dt("2026-04-01T00:00:00Z"))]
        self.assertEqual(ids, ["new"])

    def test_unknown_new_memory_does_not_hide_old_in_past(self):
        old = Memory(id="old", text="answer preference long", learned_at="2026-01-01T00:00:00Z")
        new = Memory(
            id="new",
            text="answer preference concise",
            learned_at="2026-03-01T00:00:00Z",
            supersedes=("old",),
        )
        ids = [m.id for m in active_memories([old, new], known_at=dt("2026-02-01T00:00:00Z"))]
        self.assertEqual(ids, ["old"])

    def test_lexical_retrieval_abstains_without_overlap(self):
        m = Memory(id="m", text="likes Python", learned_at="2026-01-01T00:00:00Z")
        self.assertEqual(retrieve("favorite movie", [m]), [])

    def test_retrieval_orders_by_overlap(self):
        a = Memory(id="a", text="concise answers", learned_at="2026-01-01T00:00:00Z")
        b = Memory(id="b", text="concise technical answers", learned_at="2026-01-01T00:00:00Z")
        result = retrieve("concise technical", [a, b])
        self.assertEqual([m.id for m in result], ["b", "a"])


if __name__ == "__main__":
    unittest.main()
