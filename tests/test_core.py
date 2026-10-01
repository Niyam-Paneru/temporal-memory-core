import unittest
from datetime import datetime, timezone

from temporal_memory import Memory, retrieve


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class RetrievalContractTests(unittest.TestCase):
    def test_current_retrieval_uses_the_new_eligible_preference(self):
        memories = [
            Memory(
                id="old",
                text="answer preference long",
                learned_at="2026-01-01T00:00:00Z",
            ),
            Memory(
                id="new",
                text="answer preference concise technical",
                learned_at="2026-03-01T00:00:00Z",
                supersedes=("old",),
            ),
            Memory(
                id="private-eval",
                text="answer preference concise technical",
                learned_at="2026-03-01T00:00:00Z",
                allowed_use=frozenset({"evaluation"}),
            ),
        ]

        result = retrieve(
            "concise technical answer preference",
            memories,
            known_at=dt("2026-04-01T00:00:00Z"),
            at=dt("2026-04-01T00:00:00Z"),
            required_use="retrieval",
        )

        self.assertEqual([memory.id for memory in result], ["new"])

    def test_historical_retrieval_does_not_leak_future_supersession(self):
        memories = [
            Memory(
                id="old",
                text="answer preference long",
                learned_at="2026-01-01T00:00:00Z",
            ),
            Memory(
                id="new",
                text="answer preference concise",
                learned_at="2026-03-01T00:00:00Z",
                supersedes=("old",),
            ),
        ]

        result = retrieve(
            "answer preference long",
            memories,
            known_at=dt("2026-02-01T00:00:00Z"),
            at=dt("2026-02-01T00:00:00Z"),
        )

        self.assertEqual([memory.id for memory in result], ["old"])


if __name__ == "__main__":
    unittest.main()
