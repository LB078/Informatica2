import unittest
from catch import Catch
from datetime import datetime


class TestCatch(unittest.TestCase):

    def test_default_weight(self):
        catch = Catch(1, 1, 1, "2025-01-14 16:57:00", 12, -14, "NL", 400, 70)

        self.assertEqual(
            catch.get_weight_in_local_units(), "400.00 Gram, 0.40 Kilogram"
        )

    def test_pounds_and_ounces(self):
        catch = Catch(2, 2, 2, "2025-01-14 17:08:00", 12, -14, "US", 400, 70)

        self.assertEqual(
            catch.get_weight_in_local_units(),
            "0.88 Pound, 14.10 Ounce",
        )

    def test_day_part_night(self):
        catch = Catch(3, 3, 3, datetime(2025, 1, 15, 2, 0), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Night")

    def test_day_part_morning(self):
        catch = Catch(4, 4, 4, datetime(2025, 1, 15, 11, 0), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Morning")

    def test_day_part_afternoon(self):
        catch = Catch(5, 5, 5, datetime(2025, 1, 15, 14, 49), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Afternoon")

    def test_day_part_evening(self):
        catch = Catch(6, 6, 6, datetime(2025, 1, 15, 22, 49), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Evening")

    def test_day_part_night_border(self):
        catch = Catch(7, 7, 7, datetime(2025, 1, 15, 5, 59), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Night")

    def test_day_part_morning_border(self):
        catch = Catch(8, 8, 8, datetime(2025, 1, 15, 11, 59), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Morning")

    def test_day_part_afternoon_border(self):
        catch = Catch(9, 9, 9, datetime(2025, 1, 15, 17, 59), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Afternoon")

    def test_day_part_evening_border(self):
        catch = Catch(10, 10, 10, datetime(2025, 1, 15, 23, 59), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_day_part(), "Evening")

    def test_season_spring(self):
        catch = Catch(11, 11, 11, datetime(2025, 3, 1, 12, 00), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_season(), "Spring")

    def test_season_summer(self):
        catch = Catch(11, 11, 11, datetime(2025, 6, 1, 12, 00), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_season(), "Summer")

    def test_season_autumn(self):
        catch = Catch(11, 11, 11, datetime(2025, 9, 1, 12, 00), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_season(), "Autumn")

    def test_season_winter(self):
        catch = Catch(11, 11, 11, datetime(2025, 12, 1, 12, 00), 12, -14, "US", 400, 70)

        self.assertEqual(catch.get_season(), "Winter")

    def test_weight_category_light(self):
        catch = Catch(
            12, 12, 12, datetime(2025, 12, 1, 12, 00), 12, -14, "US", 6300, 70
        )

        self.assertEqual(catch.get_weight_category(), "light")

    def test_weight_category_average(self):
        catch = Catch(
            13, 13, 13, datetime(2025, 12, 1, 12, 00), 12, -14, "US", 6450, 70
        )

        self.assertEqual(catch.get_weight_category(), "average")

    def test_weight_category_heavy(self):
        catch = Catch(
            14, 14, 14, datetime(2025, 12, 1, 12, 00), 12, -14, "US", 6600, 70
        )

        self.assertEqual(catch.get_weight_category(), "heavy")


if __name__ == "__main__":
    unittest.main()
