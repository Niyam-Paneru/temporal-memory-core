import unittest
from datetime import datetime, timezone

from temporal_memory import Memory, active_memories, retrieve


AS_OF = datetime(2026, 4, 1, tzinfo=timezone.utc)


def visible(*memories: Memory) -> list[str]:
    return [
        memory.id
        for memory in active_memories(memories, at=AS_OF, known_at=AS_OF)
    ]


class SupersessionRegressionTests(unittest.TestCase):
    def test_older_record_cannot_supersede_newer_record(self):
        old = Memory(
            id="old",
            text="favorite editor vim",
            learned_at="2026-01-01T00:00:00Z",
            supersedes=("new",),
        )
        new = Memory(
            id="new", text="favorite editor vscode", learned_at="2026-03-01T00:00:00Z"
        )

        self.assertEqual(visible(old, new), ["old", "new"])
        self.assertEqual(
            [
                memory.id
                for memory in retrieve(
                    "favorite editor", [old, new], at=AS_OF, known_at=AS_OF
                )
            ],
            ["new", "old"],
        )

    def test_self_supersession_does_not_erase_the_only_memory(self):
        memory = Memory(
            id="self",
            text="reliable",
            learned_at="2026-01-01T00:00:00Z",
            supersedes=("self",),
        )
        self.assertEqual(visible(memory), ["self"])

    def test_equal_knowledge_time_is_not_newer_even_with_different_offsets(self):
        old = Memory(id="old", text="first", learned_at="2026-01-01T00:00:00Z")
        peer = Memory(
            id="peer",
            text="second",
            learned_at="2026-01-01T05:45:00+05:45",
            supersedes=("old",),
        )
        self.assertEqual(visible(old, peer), ["old", "peer"])

    def test_later_learned_correction_can_be_backdated_in_world_time(self):
        old = Memory(id="old", text="old claim", learned_at="2026-01-01T00:00:00Z")
        correction = Memory(
            id="new",
            text="corrected claim",
            learned_at="2026-03-01T00:00:00Z",
            valid_from="2025-12-01T00:00:00Z",
            supersedes=("old",),
        )
        self.assertEqual(visible(old, correction), ["new"])

        february = datetime(2026, 2, 1, tzinfo=timezone.utc)
        self.assertEqual(
            [
                memory.id
                for memory in active_memories(
                    [old, correction], at=february, known_at=february
                )
            ],
            ["old"],
        )

    def test_ineligible_newer_record_cannot_supersede(self):
        old = Memory(id="old", text="old", learned_at="2026-01-01T00:00:00Z")
        correction = Memory(
            id="new",
            text="new",
            learned_at="2026-03-01T00:00:00Z",
            supersedes=("old",),
            allowed_use=frozenset({"evaluation"}),
        )
        self.assertEqual(visible(old, correction), ["old"])


if __name__ == "__main__":
    unittest.main()
