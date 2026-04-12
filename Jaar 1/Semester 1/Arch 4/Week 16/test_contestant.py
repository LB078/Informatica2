import unittest
from contestant import Contestant
from datetime import date


class TestContestant(unittest.TestCase):

    def test_get_age_now(self):
        contestant = Contestant("1", "Lukas", "Bellaart", "Goat", date(2004, 11, 22))
        self.assertEqual(contestant.get_age(), 20)

    def test_age_before_birthday(self):
        contestant = Contestant("1", "Lukas", "Bellaart", "Goat", date(2004, 11, 22))
        self.assertEqual(contestant.get_age(date(2024, 11, 21)), 19)

    def test_age_on_birthday(self):
        contestant = Contestant("1", "Lukas", "Bellaart", "Goat", date(2004, 11, 22))
        self.assertEqual(contestant.get_age(date(2024, 11, 22)), 20)

    def test_age_after_birthday(self):
        contestant = Contestant("1", "Lukas", "Bellaart", "Goat", date(2004, 11, 22))
        self.assertEqual(contestant.get_age(date(2024, 11, 23)), 20)

    def test_negative_age(self):
        contestant = Contestant("1", "Lukas", "Bellaart", "Goat", date(2027, 11, 22))
        self.assertEqual(contestant.get_age(), -3)


if __name__ == "__main__":
    unittest.main()
