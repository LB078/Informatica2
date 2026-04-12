# Consider a valid license plate in The Netherlands (see valid patterns below).
# Write a program that begins by reading a string of characters from the user.
# Then your program should display a message indicating whether the characters are representing a valid license plate.

# Valid patterns:
# XX-99-99
# 99-99-XX
# 99-XX-99
# XX-99-XX
# XX-XX-99
# 99-XX-XX
# 99-XXX-9
# 9-XXX-99
# XX-999-X
# X-999-XX
# XXX-99-X
# 9-XX-999
# Input examples:
# License: A-149-HH
# License: 149-A-HH
# Output examples:
# Valid
# Invalid

criteria = (
    "XX-99-99",
    "99-99-XX",
    "99-XX-99",
    "XX-99-XX",
    "XX-XX-99",
    "99-XX-XX",
    "99-XXX-9",
    "9-XXX-99",
    "XX-999-X",
    "X-999-XX",
    "XXX-99-X",
    "9-XX-999",
)

MAX_LENGTH = 9
MIN_LENGTH = 8
HYPHENS = 3


def is_valid_input(value):
    if len(value) > MAX_LENGTH:
        return False, f"License plate must not be longer than {MAX_LENGTH}"

    if len(value) < MIN_LENGTH:
        return False, f"License plate must be longer than {MIN_LENGTH}"

    if not len(value.split("-")) == HYPHENS:
        return False, f"License plate must have {HYPHENS} hyphens"

    return True, ""


def main():
    license_plate = input("License plate: ")

    valid_input, message = is_valid_input(license_plate)

    if not valid_input:
        print(message)
        return

    license_plate_found = False
    license_plate_sections = license_plate.split("-")

    for criterion in criteria:
        if license_plate_found:
            break

        criterion_sections = criterion.split("-")

        for index, section in enumerate(criterion_sections):
            if len(section) != len(license_plate_sections[index]):
                break

            if not section.isnumeric() == license_plate_sections[index].isnumeric():
                break

            if index == len(criterion_sections) - 1:
                license_plate_found = True

    if license_plate_found:
        print("valid")
    else:
        print("invalid")


if __name__ == "__main__":
    main()
