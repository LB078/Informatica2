from datetime import datetime, timedelta
from math import ceil

# ParkedCar class to store information of parked cars.


def round_to_hour(delta: timedelta):
    total_seconds = delta.total_seconds()
    hours = total_seconds / 3600

    return int(ceil(hours))


class ParkedCar:
    license_plate: str
    check_in: datetime

    def __init__(self, license_plate: str, check_in: datetime) -> None:
        self.license_plate = license_plate
        self.check_in = check_in


# Day car parking machine. Max parking fee is 24 hours (hourly_rate * 24).


class CarParkingMachine:
    capacity: int
    hourly_rate: float
    parked_cars: dict[str, ParkedCar]

    def __init__(
        self,
        capacity: int = 10,
        hourly_rate: float = 2.50,
    ) -> None:
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.parked_cars = dict()

    def check_in(self, license_plate: str, check_in: datetime | None = None) -> bool:
        "Check the car in"

        if not check_in:
            check_in = datetime.now()

        if self.parked_cars.get(license_plate):
            return False

        if len(self.parked_cars) == self.capacity:
            return False

        parked_car = ParkedCar(license_plate, check_in)

        self.parked_cars[license_plate] = parked_car

        return True

    def check_out(self, license_plate: str) -> bool:
        parked_car = self.parked_cars.get(license_plate)
        if not parked_car:
            return False

        price = self.get_parking_fee(license_plate)

        self.parked_cars.pop(license_plate)

        return price

    def get_parking_fee(self, license_plate: str) -> float:
        parked_car = self.parked_cars.get(license_plate)
        if not parked_car:
            return 0

        check_in_time = parked_car.check_in

        time = min(round_to_hour(datetime.now() - check_in_time), 24)

        return time * self.hourly_rate


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


# build menu structure as following
# the input can be case-insensitive (so E and e are valid inputs)
# [I] Check-in car by license plate
# [O] Check-out car by license plate
# [Q] Quit program
def main():
    print("[I] Check-in car by license plate")
    print("[O] Check-out car by license plate")
    print("[Q] Quit program")

    parking_machine = CarParkingMachine()

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
