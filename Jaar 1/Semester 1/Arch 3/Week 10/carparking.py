# Our car parking machine from the previous assignment is a success. But to roll our system to more parking garages in the city we need some changes and improvements that are not yet in the current system.

# When the system restarts for whatever reason we want to continue with the already parked cars.
# We want to keep track of all the parking actions in a central system and want to know in which parking garage the action has happened.
# For this assignment you are going to expand your carparking program to handle file reading and writing.

# Two new additions need to be added to the existing program from week 09 which will be explained in depth below.

# Extend Class CarParkingMachine:
# Attributes/Fields:
# id (string) - to identify this machine.
# Extra:
# When initializing a car parking machine you should load all non checked-out cars (checked-in but not checked-out) from the log file for this specific machine (example 'North'). Be sure to not check-in these cars again (as this will create new log lines), but only load them in the car parking machine instance/object.


# Class CarParkingLogger:
# Info:
# Create a new class named CarParkingLogger which contains (at least) a method to log a car check-in and a method to log a car check-out. The class should use an id to identify for which parking machine this logger is.
# Every check-in and check-out should write a line to a logfile named 'carparklog.txt' which is shared by all car parking machines. The lines should be written in a specific format as shown in the following examples:

# Attributes/Fields:
# id (string) - to identify this machine.
# Methods:
# get_machine_fee_by_day that receives the car_parking_machine_id as str (case-insensitive) and a search_date as str with format (DD-MM-YYYY). It should return the total parking fee for a specific car parking machine on a specific day rounded up to two decimals.
# get_total_car_fee that receives the license_plate as str and returns the total fee independent of the car parking machine used and should be rounded up to two decimals
# Examples:
# Car parking machine North with a parking fee rate of 2 euro per hour checks in a car with license_plate SG-123-B on February 9 at 14:33:54 (hours, minutes, seconds)

# This should result in the following log line:
# 09-02-2022 14:33:54;cpm_name=North;license_plate=SG-123-B;action=check-in

# Car parking machine North checks the same car out at 16:50:02

# This should result in the following log line:
# 09-02-2022 16:50:02;cpm_name=North;license_plate=SG-123-B;action=check-out;parking_fee=6

# Extra:
# Hint: use the datetime module to modify your datetime to the correct format.

# To test your code, use the test file from the assignment of week 09. Make sure to use os.getcwd() to get the current absolute directory sys.path[0] will not work
from datetime import datetime, timedelta
from math import ceil
import os


# ParkedCar class to store information of parked cars.
class ParkedCar:
    license_plate: str
    check_in: datetime

    def __init__(self, license_plate: str, check_in: datetime) -> None:
        self.license_plate = license_plate
        self.check_in = check_in


class CarParkingLogger:
    LOG_FILE = "carparklog.txt"
    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def _read_log_file() -> list[str]:
        """Reads the car park log file and returns its content as a list of lines."""
        file_path = os.path.join(os.getcwd(), CarParkingLogger.LOG_FILE)
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            return [line.strip() for line in file]

    @staticmethod
    def _write_to_log_file(entry: str) -> None:
        """Writes a log entry to the car park log file."""
        file_path = os.path.join(os.getcwd(), CarParkingLogger.LOG_FILE)
        with open(file_path, "a") as file:
            file.write(entry + "\n")

    def get_machine_fee_by_day(
        self, car_parking_machine_id: str, search_date: str
    ) -> float:
        lines = (self._read_log_file())

        filtered_lines = filter(
            lambda x: f"cpm_name={car_parking_machine_id}" in x
            and search_date in x
            and "parking_fee" in x,
            lines,
        )

        return round(
            sum([float(line.split(";")[4].split("=")[1])
                for line in filtered_lines]), 2
        )

    def get_total_car_fee(self, license_plate: str) -> float:
        lines = (self._read_log_file())
        filtered_lines = filter(
            lambda x: f"license_plate={
                license_plate}" in x and "parking_fee" in x,
            lines,
        )

        return round(
            sum([float(line.split(";")[4].split("=")[1])
                for line in filtered_lines]), 2
        )

    def get_parked_cars(
        self, car_parking_machine_id: str
    ) -> list[tuple[str, datetime]]:
        with open(os.getcwd() + "/carparklog.txt", "r") as file:
            lines = [line.strip() for line in file.readlines()]
            filtered_lines = filter(
                lambda x: f"cpm_name={car_parking_machine_id}" in x, lines
            )

            parked_cars: list[tuple[str, datetime]] = []

            # check if cars with status check-in dont have check-out
            for line in filtered_lines:
                parts = {
                    key: value
                    for key, value in (item.split("=") for item in line.split(";")[1:])
                }

                check_in_time = datetime.strptime(
                    line.split(";")[0], "%d-%m-%Y %H:%M:%S")

                action = parts.get("action")
                license_plate = parts.get("license_plate")

                if action == "check-in":
                    parked_cars.append((license_plate, check_in_time))

                if action == "check-out":
                    parked_cars = [
                        car for car in parked_cars if license_plate not in car
                    ]

            return parked_cars

    def log_check_in(
        self, cpm_name: str, license_plate: str, check_in_time: datetime
    ) -> None:
        self._write_to_log_file(
            f"""{check_in_time.strftime('%d-%m-%Y %H:%M:%S')};cpm_name={
                cpm_name};license_plate={license_plate};action=check-in\n"""
        )

    def log_check_out(
        self,
        cpm_name: str,
        license_plate: str,
        check_out_time: datetime,
        parking_fee: float,
    ) -> None:
        self._write_to_log_file(
            f"""{check_out_time.strftime('%d-%m-%Y %H:%M:%S')};cpm_name={cpm_name};license_plate={
                license_plate};action=check-out;parking_fee={parking_fee}\n"""
        )


# Day car parking machine. Max parking fee is 24 hours (hourly_rate * 24).
class CarParkingMachine:
    id: str
    capacity: int
    hourly_rate: float
    parked_cars: dict[str, ParkedCar]
    logger: CarParkingLogger

    def __init__(
        self,
        id: str,
        capacity: int = 10,
        hourly_rate: float = 2.50,
    ) -> None:
        self.id = id
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.parked_cars = dict()
        self.logger = CarParkingLogger(id)

        for parked_car in self.logger.get_parked_cars(self.id):
            self.parked_cars[parked_car[0]] = ParkedCar(
                parked_car[0], parked_car[1])

    @staticmethod
    def _round_to_hour(delta: timedelta):
        total_seconds = delta.total_seconds()
        hours = total_seconds / 3600

        return int(ceil(hours))

    def check_in(
        self, license_plate: str, check_in: datetime | None = None, log: bool = True
    ) -> bool:
        "Check the car in"

        if not check_in:
            check_in = datetime.now()

        if self.parked_cars.get(license_plate):
            return False

        if len(self.parked_cars) == self.capacity:
            return False

        parked_car = ParkedCar(license_plate, check_in)

        self.parked_cars[license_plate] = parked_car

        self.logger.log_check_in(self.id, license_plate, check_in)

        return True

    def check_out(self, license_plate: str) -> bool:
        "Check the car out"
        parked_car = self.parked_cars.get(license_plate)
        if not parked_car:
            return False

        price = self.get_parking_fee(license_plate)

        self.parked_cars.pop(license_plate)

        self.logger.log_check_out(
            self.id, license_plate, datetime.now(), price)

        return price

    def get_parking_fee(self, license_plate: str) -> float:
        "Get the parking fee for the car"
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
