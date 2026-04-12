from carparking import CarParkingMachine
from datetime import datetime, timedelta
from unittest import TestCase, main
import sqlite3
import os
import sys


class TestParking(TestCase):
    connection = sqlite3.connect(os.path.join(sys.path[0], "carparkingmachine.db"))
    cursor = connection.cursor()

    def setUp(self):

        reset_query = """
        DROP TABLE IF EXISTS parkings
        """
        self.cursor.execute(reset_query)
        self.connection.commit()

    # Test for a normal check-in with correct result (True)
    def test_check_in_capacity_normal(self):
        parking_machine_name = "Queens"
        parking_machine = CarParkingMachine(parking_machine_name)
        self.assertTrue(parking_machine.check_in("AAA-10-BB"))

        select_query = """
        SELECT count(id)
        FROM parkings
        WHERE car_parking_machine = ?
        """

        self.cursor.execute(select_query, (parking_machine_name,))

        selected_rows = self.cursor.fetchone()

        self.assertEqual(selected_rows[0], 1)
        self.assertEqual(len(parking_machine.parked_cars), 1)

    # Test for a check-in with maximum capacity reached (False)
    def test_check_in_capacity_reached(self):
        parking_machine = CarParkingMachine("Brooklyn")
        for i in range(10):
            self.assertTrue(parking_machine.check_in(f"AAA-{i}-BB"))

        self.assertTrue(parking_machine.capacity == len(parking_machine.parked_cars))
        self.assertFalse(parking_machine.check_in("AAA-20-BB"))

    # Test for checking the correct parking fees
    def test_parking_fee(self):
        parking_machine = CarParkingMachine("Bronx")

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
        parking_machine_name = "Manhattan"
        parking_machine = CarParkingMachine(parking_machine_name)

        check_in_time = datetime.now() - timedelta(hours=2, minutes=10)

        parking_machine.check_in("AAA-10-BB", check_in_time)

        select_query = """
        SELECT count(id)
        FROM parkings
        WHERE car_parking_machine = ? AND license_plate = ? AND parking_fee = 0
        """

        self.cursor.execute(select_query, (parking_machine_name, "AAA-10-BB"))

        selected_rows = self.cursor.fetchone()

        # Assert that {license_plate} is in parked_cars
        self.assertEqual(selected_rows[0], 1)
        self.assertIn("AAA-10-BB", parking_machine.parked_cars)

        # Assert that correct parking fee is provided when checking-out {license_plate}
        self.assertEqual(parking_machine.check_out("AAA-10-BB"), 7.5)

        select_query = """
        SELECT count(id)
        FROM parkings
        WHERE car_parking_machine = ? AND license_plate = ? AND parking_fee = 0
        """

        self.cursor.execute(select_query, (parking_machine_name, "AAA-10-BB"))

        selected_rows = self.cursor.fetchone()

        # Assert that {license_plate} is no longer in parked_cars
        self.assertEqual(selected_rows[0], 0)
        self.assertNotIn("AAA-10-BB", parking_machine.parked_cars)


if __name__ == "__main__":
    main()
