from carparking import CarParkingLogger
import csv
import os
import sys


def get_input(prompt: str, validation_function) -> str:
    """Get input from user with validation"""
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def create_csv_file(file_name: str, headers: list[str], data: list[list[str]]):
    """Create a csv file with the given file name, headers and data"""
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)
        writer.writerows(data)


def main():
    print(
        "[P] Report all parked cars during a parking period for a specific parking machine"
    )
    print(
        "[F] Report total collected parking fee during a parking period for all parking machines"
    )
    print("[Q] Quit program")

    while True:
        menu_choice = get_input(
            "Choice? ", lambda x: x.lower() in ["p", "f", "q"]
        ).lower()

        match menu_choice:
            case "p":
                input_data = get_input(
                    "Enter car parking machine identifier, from date, to date: ",
                    lambda x: len(x.split(",")) == 3,
                )

                # input_data = "North,18-11-2024,19-11-2024"

                cpm_id, from_date, to_date = [
                    item.strip() for item in input_data.split(",")
                ]

                logger = CarParkingLogger(cpm_id)

                parked_cars = logger.report_parked_cars(cpm_id, from_date, to_date)
                parked_cars.sort(key=lambda x: x[0])

                csv_data = [
                    [
                        car[0],
                        car[1].strftime("%d-%m-%Y %H:%M:%S"),
                        (
                            car[2].strftime("%d-%m-%Y %H:%M:%S")
                            if car[2] is not None
                            else "None"
                        ),
                        car[3],
                    ]
                    for car in parked_cars
                ]

                file_name = os.path.join(
                    sys.path[0],
                    f"parkedcars_{cpm_id}_from_{from_date}_to_{to_date}.csv",
                )

                create_csv_file(
                    file_name,
                    ["license_plate", "checked_in", "checked_out", "parking_fee"],
                    csv_data,
                )
            case "f":
                input_data = get_input(
                    "Enter from date, to date: ", lambda x: len(x.split(",")) == 2
                )

                from_date, to_date = [item.strip() for item in input_data.split(",")]
                logger = CarParkingLogger("1")

                total_fees = logger.report_total_fees(from_date, to_date)

                file_name = os.path.join(
                    sys.path[0], f"totalfee_from_{from_date}_to_{to_date}.csv"
                )

                csv_data = [
                    [machines[0], machines[1]] for machines in total_fees.items()
                ]
                create_csv_file(
                    file_name, ["car_parking_machine", "total_parking_fee"], csv_data
                )
            case "q":
                break


if __name__ == "__main__":
    main()
