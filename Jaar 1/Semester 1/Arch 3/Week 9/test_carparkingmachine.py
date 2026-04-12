from carparking import CarParkingMachine
from datetime import datetime, timedelta
from unittest import TestCase, main


class TestParking(TestCase):
    # Test for a normal check-in with correct result (True)
    def test_check_in_capacity_normal(self):
        parking_machine = CarParkingMachine()
        self.assertTrue(parking_machine.check_in("AAA-10-BB"))
        self.assertEqual(len(parking_machine.parked_cars), 1)

    # Test for a check-in with maximum capacity reached (False)
    def test_check_in_capacity_reached(self):
        parking_machine = CarParkingMachine()
        for i in range(10):
            self.assertTrue(parking_machine.check_in(f"AAA-{i}-BB"))

        self.assertTrue(parking_machine.capacity == len(parking_machine.parked_cars))
        self.assertFalse(parking_machine.check_in("AAA-20-BB"))

    # Test for checking the correct parking fees
    def test_parking_fee(self):
        parking_machine = CarParkingMachine()

        # Assert that parking time 2h10m, gives correct parking fee
        first_test_datetime = datetime.now() - timedelta(hours=2, minutes=10)
        parking_machine.check_in("AAA-10-BB", first_test_datetime)

        self.assertEqual(parking_machine.check_out("AAA-10-BB"), 7.5)

        # Assert that parking time 24h, gives correct parking fee
        second_test_datetime = datetime.now() - timedelta(hours=24)
        parking_machine.check_in("AAA-20-BB", second_test_datetime)

        self.assertEqual(parking_machine.check_out("AAA-20-BB"), 60)

        # Assert that parking time 30h == 24h max, gives correct parking fee
        third_test_datetime = datetime.now() - timedelta(hours=30)
        parking_machine.check_in("AAA-30-BB", third_test_datetime)
        self.assertEqual(parking_machine.check_out("AAA-30-BB"), 60)

    # Test for validating check-out behaviour
    def test_check_out(self):
        parking_machine = CarParkingMachine()

        check_in_time = datetime.now() - timedelta(hours=2, minutes=10)

        # Assert that {license_plate} is in parked_cars
        parking_machine.check_in("AAA-10-BB", check_in_time)
        self.assertIn("AAA-10-BB", parking_machine.parked_cars)

        # Assert that correct parking fee is provided when checking-out {license_plate}
        self.assertEqual(parking_machine.check_out("AAA-10-BB"), 7.5)

        # Assert that {license_plate} is no longer in parked_cars
        self.assertNotIn("AAA-10-BB", parking_machine.parked_cars)


if __name__ == "__main__":
    main()
