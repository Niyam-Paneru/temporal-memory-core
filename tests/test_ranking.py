import unittest

from temporal_memory.models import Memory
from temporal_memory.ranking import lexical_score, retrieve


class RankingTests(unittest.TestCase):
    def test_no_overlap_abstains(self):
        memory = Memory(id="m", text="likes Python", learned_at="2026-01-01T00:00:00Z")
        self.assertEqual(retrieve("favorite movie", [memory]), [])

    def test_more_overlap_ranks_first(self):
        a = Memory(id="a", text="concise answers", learned_at="2026-01-01T00:00:00Z")
        b = Memory(id="b", text="concise technical answers", learned_at="2026-01-01T00:00:00Z")
        self.assertEqual([m.id for m in retrieve("concise technical", [a, b])], ["b", "a"])

    def test_score_is_auditable(self):
        memory = Memory(id="m", text="python backend systems", learned_at="2026-01-01T00:00:00Z")
        self.assertEqual(lexical_score("python systems", memory), 2)


if __name__ == "__main__":
    unittest.main()
