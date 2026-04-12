import os
import sys

valid_lines = list()
corrupt_lines = list()


def is_valid_date(date: str) -> bool:
    year, month, day = map(int, date.split("-"))
    return (1960 <= year <= 2004) and (1 <= month <= 12) and (1 <= day <= 31)


def validate_data(line: str) -> None:
    student_number, first_name, last_name, birth_date, student_program = line.split(
        ",")

    invalid_data = list()

    if not (student_number.startswith("08") or student_number.startswith("09")):
        invalid_data.append(student_number)

    if not first_name.isalpha():
        invalid_data.append(first_name)

    if not last_name.replace(" ", "").replace("'", "").isalpha():
        invalid_data.append(last_name)

    if not is_valid_date(birth_date):
        invalid_data.append(birth_date)

    if student_program not in {"INF", "TINF", "CMD", "AI"}:
        invalid_data.append(student_program)

    if len(invalid_data) == 0:
        valid_lines.append(line)
    else:
        corrupt_lines.append(f"{line} => INVALID DATA: {invalid_data}")


def main(csv_file):
    with open(os.path.join(sys.path[0], csv_file), newline="") as csv_file:
        # skip header line
        next(csv_file)

        for line in csv_file:
            validate_data(line.strip())

    print("### VALID LINES ###")
    print("\n".join(valid_lines))
    print("### CORRUPT LINES ###")
    print("\n".join(corrupt_lines))


if __name__ == "__main__":
    main("students.csv")
