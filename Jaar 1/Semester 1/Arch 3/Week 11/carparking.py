from datetime import datetime, timedelta
from math import ceil
import os
import sys
import json


# ParkedCar class to store information of parked cars.
class ParkedCar:
    license_plate: str
    check_in: datetime

    def __init__(self, license_plate: str, check_in: datetime) -> None:
        self.license_plate = license_plate
        self.check_in = check_in


class CarParkingLogger:
    LOG_FILE_PATH = os.path.join(sys.path[0], "carparklog.txt")
    state_file_path: str
    id: str

    def __init__(self, id: str) -> None:
        self.id = id
        self.state_file_path = os.path.join(sys.path[0], id + "_state.json")

    @staticmethod
    def _read_log_file() -> list[str]:
        """Reads the car park log file and returns its content as a list of lines."""
        if not os.path.exists(CarParkingLogger.LOG_FILE_PATH):
            return []
        with open(CarParkingLogger.LOG_FILE_PATH, "r") as file:
            return [line.strip() for line in file]

    @staticmethod
    def _write_to_log_file(entry: str) -> None:
        """Writes a log entry to the car park log file."""
        with open(CarParkingLogger.LOG_FILE_PATH, "a") as file:
            file.write(entry + "\n")

    def save_state(self, state: dict[str, ParkedCar]) -> None:
        """Saves the state of the car parking machine to the log file."""
        cars = [
            {
                "license_plate": car.license_plate,
                "check_in": car.check_in.strftime("%d-%m-%Y %H:%M:%S"),
            }
            for car in state.values()
        ]

        with open(self.state_file_path, "w") as file:
            json.dump(cars, file)

    def load_state(self) -> dict[str, ParkedCar]:
        """Loads the state of the car parking machine from the log file."""
        if not os.path.exists(self.state_file_path):
            return {}

        with open(self.state_file_path, "r") as file:
            return {
                car["license_plate"]: ParkedCar(
                    car["license_plate"],
                    datetime.strptime(car["check_in"], "%d-%m-%Y %H:%M:%S"),
                )
                for car in json.load(file)
            }

    def get_machine_fee_by_day(
        self, car_parking_machine_id: str, search_date: str
    ) -> float:
        """Returns the total parking fee for a specific car parking machine on a specific day."""
        lines = self._read_log_file()

        filtered_lines = filter(
            lambda x: f"cpm_name={car_parking_machine_id}" in x
            and search_date in x
            and "parking_fee" in x,
            lines,
        )

        return round(
            sum([float(line.split(";")[4].split("=")[1]) for line in filtered_lines]), 2
        )

    def get_total_car_fee(self, license_plate: str) -> float:
        """Returns the total parking fee for a specific car."""
        lines = self._read_log_file()
        filtered_lines = filter(
            lambda x: f"license_plate={license_plate}" in x and "parking_fee" in x,
            lines,
        )

        return round(
            sum([float(line.split(";")[4].split("=")[1]) for line in filtered_lines]), 2
        )

    def log_check_in(
        self, cpm_name: str, license_plate: str, check_in_time: datetime
    ) -> None:
        """Logs a check-in event to the car park log file."""
        self._write_to_log_file(
            f"""{check_in_time.strftime('%d-%m-%Y %H:%M:%S')};cpm_name={cpm_name};license_plate={license_plate};action=check-in\n"""
        )

    def log_check_out(
        self,
        cpm_name: str,
        license_plate: str,
        check_out_time: datetime,
        parking_fee: float,
    ) -> None:
        """Logs a check-out event to the car park log file."""
        self._write_to_log_file(
            f"""{check_out_time.strftime('%d-%m-%Y %H:%M:%S')};cpm_name={cpm_name};license_plate={license_plate};action=check-out;parking_fee={parking_fee}\n"""
        )

    def report_parked_cars(
        self, cpm_id: str, from_date: str, to_date: str
    ) -> list[list[str, datetime, datetime | None, float]]:
        """Reports all parked cars during a parking period for a specific parking machine."""
        from_datetime = datetime.strptime(from_date, "%d-%m-%Y")
        to_datetime = datetime.strptime(to_date, "%d-%m-%Y")
        log_entries = self._read_log_file()
        filtered_lines = filter(
            lambda x: f"cpm_name={cpm_id}" in x
            and from_datetime
            <= datetime.strptime(x.split(";")[0], "%d-%m-%Y %H:%M:%S")
            <= to_datetime,
            log_entries,
        )

        parked_cars: list[list[str, datetime, datetime | None, float]] = []

        for line in filtered_lines:
            parts = {
                key: value
                for key, value in (item.split("=") for item in line.split(";")[1:])
            }

            check_in_time = datetime.strptime(line.split(";")[0], "%d-%m-%Y %H:%M:%S")
            action = parts.get("action")
            license_plate = parts.get("license_plate")

            if action == "check-in":
                parked_cars.append([license_plate, check_in_time, None, 0])

            if action == "check-out":
                check_out_time = datetime.strptime(
                    line.split(";")[0], "%d-%m-%Y %H:%M:%S"
                )
                parking_fee = float(parts.get("parking_fee"))
                for parked_car in parked_cars:
                    if parked_car[0] == license_plate and parked_car[2] is None:
                        parked_car[2] = check_out_time
                        parked_car[3] = parking_fee

        return parked_cars

    def report_total_fees(self, from_date: str, to_date: str) -> dict[str, float]:
        """Reports total collected parking fee during a parking period for all parking machines."""
        from_datetime = datetime.strptime(from_date, "%d-%m-%Y")
        to_datetime = datetime.strptime(to_date, "%d-%m-%Y")
        log_entries = self._read_log_file()
        machines = {}

        for entry in log_entries:
            parts = entry.split(";")
            timestamp = datetime.strptime(parts[0], "%d-%m-%Y %H:%M:%S")

            if (
                from_datetime <= timestamp <= to_datetime
                and "action=check-out" in parts
            ):
                machine_name = parts[1].split("=")[1]
                fee = float(parts[4].split("=")[1])
                machines[machine_name] = machines.get(machine_name, 0) + fee

        return machines


# Day car parking machine. Max parking fee is 24 hours (hourly_rate * 24).
checked_in_cars = set()


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
        self.logger = CarParkingLogger(id)
        self.parked_cars = self.logger.load_state()

        for parked_car in self.parked_cars.values():
            checked_in_cars.add(parked_car.license_plate)

    def _round_to_hour(self, delta: timedelta):
        """Rounds a timedelta to the nearest hour"""
        total_seconds = delta.total_seconds()
        hours = total_seconds / 3600

        return int(ceil(hours))

    def check_in(
        self, license_plate: str, check_in: datetime | None = None, log: bool = True
    ) -> bool:
        """Checks the car in"""

        if not check_in:
            check_in = datetime.now()

        if self.parked_cars.get(license_plate):
            return False

        if license_plate in checked_in_cars:
            return False

        if len(self.parked_cars) == self.capacity:
            return False

        parked_car = ParkedCar(license_plate, check_in)

        checked_in_cars.add(license_plate)
        self.parked_cars[license_plate] = parked_car

        self.logger.log_check_in(self.id, license_plate, check_in)
        self.logger.save_state(self.parked_cars)
        return True

    def check_out(self, license_plate: str) -> bool:
        """Checks the car out"""
        parked_car = self.parked_cars.get(license_plate)
        if not parked_car:
            return False

        price = self.get_parking_fee(license_plate)

        self.parked_cars.pop(license_plate)
        checked_in_cars.remove(license_plate)

        self.logger.log_check_out(self.id, license_plate, datetime.now(), price)
        self.logger.save_state(self.parked_cars)

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
