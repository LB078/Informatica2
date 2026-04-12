from datetime import datetime, timedelta
from math import ceil
import os
import sys
import sqlite3


# ParkedCar class to store information of parked cars.
class ParkedCar:
    license_plate: str
    check_in: datetime
    id: int | None
    check_out: datetime | None
    parking_fee: float | None

    def __init__(
        self,
        license_plate: str,
        check_in: datetime,
        id: int | None = None,
        check_out: datetime | None = None,
        parking_fee: float = 0,
    ) -> None:
        self.license_plate = license_plate
        self.check_in = check_in
        self.id = id
        self.check_out = check_out
        self.parking_fee = parking_fee


class CarParkingMachine:
    id: str
    capacity: int
    hourly_rate: float
    parked_cars: dict[str, ParkedCar]
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(
        self,
        id: str,
        capacity: int = 10,
        hourly_rate: float = 2.50,
    ) -> None:
        self.id = id
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.connection = sqlite3.connect(
            os.path.join(sys.path[0], "carparkingmachine.db")
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS parkings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_parking_machine TEXT NOT NULL,
                license_plate TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT DEFAULT NULL,
                parking_fee NUMERIC DEFAULT 0
            );"""
        )
        self.connection.commit()
        self.parked_cars = self._reset_state()

    def _reset_state(self) -> dict[str, ParkedCar]:
        reset_state_query = """
            SELECT id, license_plate, check_in
            FROM parkings
            WHERE car_parking_machine = ? AND check_out IS NULL
        """

        self.cursor.execute(reset_state_query, (self.id,))

        return {
            parked_car[1]: ParkedCar(
                parked_car[1],
                datetime.strptime(parked_car[2], "%Y-%m-%d %H:%M:%S.%f"),
                parked_car[0],
            )
            for parked_car in self.cursor.fetchall()
        }

    def _insert(self, parked_car: ParkedCar) -> ParkedCar:
        insert_query = """ 
            INSERT INTO parkings (car_parking_machine, license_plate, check_in)
            VALUES (:car_parking_machine, :license_plate, :check_in)
        """

        self.cursor.execute(
            insert_query, {"car_parking_machine": self.id,
                           **parked_car.__dict__}
        )

        parked_car.id = self.cursor.lastrowid
        self.connection.commit()
        return parked_car

    def _update(self, parked_car: ParkedCar) -> None:
        update_query = """
        UPDATE parkings
        SET license_plate = :license_plate,
        check_in = :check_in,
        check_out = :check_out,
        parking_fee = :parking_fee
        WHERE id = :id
        """

        self.cursor.execute(update_query, parked_car.__dict__)

        self.connection.commit()

    def find_by_id(self, id: int) -> ParkedCar | None:
        find_by_id_query = """
        SELECT license_plate, check_in
        FROM parkings
        WHERE id = ? AND check_out IS NULL
        ORDER BY id
        DESC
        LIMIT 1
        """

        self.cursor.execute(find_by_id_query, (id,))
        found_car = self.cursor.fetchone()

        if found_car:
            return ParkedCar(found_car[0], found_car[1], id)

        return found_car

    def find_last_checkin(self, license_plate: str) -> int | None:
        find_last_checkin_query = """
        SELECT id
        FROM parkings
        WHERE license_plate = ? AND check_out IS NULL
        ORDER BY id
        DESC
        LIMIT 1
        """

        self.cursor.execute(find_last_checkin_query, (license_plate,))
        found_car = self.cursor.fetchone()

        if found_car:
            return found_car[0]

        return found_car

    def _round_to_hour(self, delta: timedelta):
        """Rounds a timedelta to the nearest hour"""
        total_seconds = delta.total_seconds()
        hours = total_seconds / 3600

        return int(ceil(hours))

    def check_in(self, license_plate: str, check_in: datetime | None = None) -> bool:
        """Checks the car in"""
        if not check_in:
            check_in = datetime.now()

        parked_car = self.parked_cars.get(license_plate)
        if parked_car:
            return False

        if self.find_last_checkin(license_plate):
            return False

        if len(self.parked_cars) == self.capacity:
            return False

        parked_car = self._insert(ParkedCar(license_plate, check_in))
        self.parked_cars[license_plate] = parked_car

        return True

    def check_out(self, license_plate: str) -> float:
        """Checks the car out"""
        parked_car = self.parked_cars.get(license_plate)
        if not parked_car:
            return False

        price = self.get_parking_fee(license_plate)

        self.parked_cars.pop(license_plate)

        parked_car.check_out, parked_car.parking_fee = datetime.now(), price

        self._update(parked_car)

        return price

    def get_parking_fee(self, license_plate: str) -> float:
        """Get the parking fee for the car"""
        parked_car = self.parked_cars.get(license_plate)
        if not parked_car:
            return 0

        check_in_time = parked_car.check_in

        time = min(self._round_to_hour(datetime.now() - check_in_time), 24)

        return time * self.hourly_rate


def get_input(prompt: str, validation_function) -> str:
    "Get input from user with validation"
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main():
    print("[I] Check-in car by license plate")
    print("[O] Check-out car by license plate")
    print("[Q] Quit program")

    parking_machine = CarParkingMachine("North")

    while True:
        menu_choice = get_input(
            "Choice? ", lambda x: x.lower() in ["i", "o", "q"]
        ).lower()

        match menu_choice:
            case "i":
                license_plate = get_input(
                    "License plate? ", lambda x: len(x) > 1
                ).upper()
                check_in_success = parking_machine.check_in(license_plate)

                if check_in_success:
                    print("License registered")
                else:
                    print("Capacity reached")
            case "o":
                license_plate = get_input(
                    "License plate? ", lambda x: len(x) > 1
                ).upper()
                parking_fee = parking_machine.check_out(license_plate)

                if parking_fee == 0:
                    print(f"License {license_plate} not found!")
                else:
                    print(f"Parking fee: {parking_fee:.2f} EUR")
            case "q":
                break


if __name__ == "__main__":
    main()
