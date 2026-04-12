from distanceconverter import Converter
from unittest import TestCase, main


class TestDistanceConverter(TestCase):
    converter = Converter(9, "inches")

    def test_inches(self):
        self.assertEqual(self.converter.inches(), 9)

    def test_feet(self):
        self.assertEqual(self.converter.feet(), 0.75)

    def test_yards(self):
        self.assertEqual(self.converter.yards(), 0.25)

    def test_miles(self):
        self.assertEqual(round(self.converter.miles(), 9), 0.000142045)

    def test_kilometers(self):
        self.assertEqual(self.converter.kilometers(), 0.0002286)

    def test_meters(self):
        self.assertEqual(self.converter.meters(), 0.2286)

    def test_centimeters(self):
        self.assertEqual(self.converter.centimeters(), 22.86)

    def test_millimeters(self):
        self.assertEqual(self.converter.millimeters(), 228.6)

    def test_default_feet(self):
        converter = Converter(9, "feet")
        self.assertEqual(round(converter.meters(), 4), 2.7432)

    def test_default_yards(self):
        converter = Converter(9, "yards")
        self.assertEqual(converter.meters(), 8.2296)

    def test_default_miles(self):
        converter = Converter(9, "miles")
        self.assertEqual(round(converter.meters(), 3), 14484.096)

    def test_default_kilometers(self):
        converter = Converter(9, "kilometers")
        self.assertEqual(converter.meters(), 9000)

    def test_default_meters(self):
        converter = Converter(9, "meters")
        self.assertEqual(converter.meters(), 9)

    def test_default_centimeters(self):
        converter = Converter(9, "centimeters")
        self.assertEqual(converter.meters(), 0.09)

    def test_default_millimeters(self):
        converter = Converter(9, "millimeters")
        self.assertEqual(round(converter.meters(), 3), 0.009)

    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            Converter(9, "invalid")


if __name__ == "__main__":
    main()
