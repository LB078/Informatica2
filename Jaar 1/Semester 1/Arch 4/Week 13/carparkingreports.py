import csv
import os
import sys
import sqlite3


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
    print(
        "[C] Report all complete parkings over all parking machines for a specific car"
    )
    print("[Q] Quit program")

    connection = sqlite3.connect(os.path.join(sys.path[0], "carparkingmachine.db"))

    cursor = connection.cursor()

    while True:
        menu_choice = get_input(
            "Choice? ", lambda x: x.lower() in ["p", "f", "q", "c"]
        ).lower()

        match menu_choice:
            case "p":
                input_data = get_input(
                    "Enter car parking machine identifier, from date, to date: ",
                    lambda x: len(x.split(",")) == 3,
                )

                cpm_id, from_date, to_date = [
                    item.strip() for item in input_data.split(",")
                ]

                query = """
                SELECT license_plate, check_in, check_out, parking_fee
                FROM parkings
                WHERE NOT parking_fee = 0 AND car_parking_machine = :cpm_id AND (check_in BETWEEN :from_date AND :to_date)
                ORDER BY check_in DESC
                """

                query_from_date = f"{from_date} 00:00:00"
                query_to_date = f"{to_date} 23:59:59"

                cursor.execute(
                    query,
                    {
                        "cpm_id": cpm_id,
                        "from_date": query_from_date,
                        "to_date": query_to_date,
                    },
                )

                parked_cars = cursor.fetchall()

                file_name = os.path.join(
                    sys.path[0],
                    f"parkedcars_{cpm_id}_from_{from_date}_to_{to_date}.csv",
                )

                create_csv_file(
                    file_name,
                    ["license_plate", "checked_in", "checked_out", "parking_fee"],
                    parked_cars,
                )
            case "f":
                input_data = get_input(
                    "Enter from date, to date: ", lambda x: len(x.split(",")) == 2
                )

                from_date, to_date = [item.strip() for item in input_data.split(",")]

                query = """
                SELECT car_parking_machine, SUM(parking_fee)
                FROM parkings
                WHERE NOT parking_fee = 0 AND (check_in BETWEEN :from_date AND :to_date)
                GROUP BY car_parking_machine
                """

                query_from_date = f"{from_date} 00:00:00"
                query_to_date = f"{to_date} 23:59:59"

                cursor.execute(
                    query,
                    {
                        "from_date": query_from_date,
                        "to_date": query_to_date,
                    },
                )

                parked_cars = cursor.fetchall()

                file_name = os.path.join(
                    sys.path[0], f"totalfee_from_{from_date}_to_{to_date}.csv"
                )

                create_csv_file(
                    file_name, ["car_parking_machine", "total_parking_fee"], parked_cars
                )
            case "c":
                license_plate = input("License plate: ").strip()

                query = """
                SELECT car_parking_machine, check_in, check_out, parking_fee
                FROM parkings
                WHERE NOT parking_fee = 0 AND license_plate = ?
                ORDER BY check_in DESC
                """

                cursor.execute(query, (license_plate,))

                complete_parkings = cursor.fetchall()

                file_name = os.path.join(
                    sys.path[0], f"all_parkings_for_{license_plate}.csv"
                )

                create_csv_file(
                    file_name,
                    ["car_parking_machine", "check_in", "check_out", "parking_fee"],
                    complete_parkings,
                )
            case "q":
                break


if __name__ == "__main__":
    main()
