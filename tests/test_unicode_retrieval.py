import unittest
from datetime import datetime, timezone

from temporal_memory import Memory, retrieve
from temporal_memory.ranking import tokens


AS_OF = datetime(2026, 4, 1, tzinfo=timezone.utc)


class UnicodeRetrievalTests(unittest.TestCase):
    def test_exact_nepali_words_remain_searchable(self):
        memory = Memory(
            id="nepali",
            text="नेपालमा पढ्ने विद्यार्थी",
            learned_at="2026-01-01T00:00:00Z",
        )
        self.assertEqual(tokens(memory.text), {"नेपालमा", "पढ्ने", "विद्यार्थी"})
        self.assertEqual(
            [m.id for m in retrieve(memory.text, [memory], at=AS_OF, known_at=AS_OF)],
            ["nepali"],
        )

    def test_different_devanagari_words_do_not_share_stripped_fragments(self):
        self.assertEqual(tokens("घरमा") & tokens("घरको"), set())

    def test_composed_and_decomposed_accents_are_equivalent(self):
        self.assertEqual(tokens("Café"), tokens("CAFE\u0301"))
        self.assertEqual(tokens("straße"), tokens("STRASSE"))
        self.assertEqual(tokens("ＦＵＬＬＷＩＤＴＨ"), {"fullwidth"})

    def test_ascii_punctuation_and_underscores_still_split_words(self):
        self.assertEqual(
            tokens("Node.js python_backend v2"),
            {"node", "js", "python", "backend", "v2"},
        )

    def test_leading_combining_mark_cannot_form_an_orphan_token(self):
        self.assertEqual(tokens("\u0301 hello"), {"hello"})

    def test_unicode_digits_and_letters_remain_words(self):
        self.assertEqual(tokens("संस्करण १२३"), {"संस्करण", "१२३"})


if __name__ == "__main__":
    unittest.main()
