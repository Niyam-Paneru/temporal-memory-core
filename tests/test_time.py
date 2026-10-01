import unittest
from datetime import datetime, timezone

from temporal_memory.time import known_by, parse_utc, valid_at


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class TimeTests(unittest.TestCase):
    def test_parse_utc_accepts_z(self):
        self.assertEqual(parse_utc("2026-01-01T00:00:00Z"), dt("2026-01-01T00:00:00Z"))

    def test_future_knowledge_is_unknown(self):
        self.assertFalse(known_by("2026-04-01T00:00:00Z", known_at=dt("2026-03-01T00:00:00Z")))

    def test_valid_until_is_exclusive(self):
        self.assertFalse(
            valid_at(
                learned_at="2026-01-01T00:00:00Z",
                valid_from=None,
                valid_until="2026-03-01T00:00:00Z",
                at=dt("2026-03-01T00:00:00Z"),
            )
        )


if __name__ == "__main__":
    unittest.main()
