# Write a program that reads a date from the user and computes its immediate successor.

# Criteria:
# The date will be entered in YYYY-MM-DD format.
# Assume there is no leap year so February always has 28 days.
# The program must employ a function is_input_valid(inp_date) that checks if the provided input satisfies the expected format. The function returns true if the input has correct format. In case of incorrect format, the function must return false.
# The program must print Input format ERROR. Correct Format: YYYY-MM-DD in case the user enters an incorrect input.

# Some examples of incorrect input: 2013/12/30, 2013_12_30, 0213/12/30, 30-12-2013.

# Input examples:
# Input Date: 2013-11-18
# Input Date: 2013-11-30
# Input Date: 2013-12-31
# Output examples:
# Next Date: 2013-11-19
# Next Date: 2013-12-01
# Next Date: 2014-01-01

end_of_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_valid_input(value):
    if not len(value.split("-")) == 3:
        return False

    year, month, day = value.split("-")

    if len(year) > 4:
        return False

    if not len(month) == 2:
        return False

    if not len(day) == 2:
        return False

    return True


def main():
    date = input("Date: ")

    if not is_valid_input(date):
        print("Input format ERROR. Correct Format: YYYY-MM-DD")
        return

    year, month, day = date.split("-")

    month = int(month)
    day = int(day)

    end_of_month = end_of_months[month - 1]

    if month == 12 and day == 31:
        print(f"Next Date: {int(year) + 1}-01-01")
        return

    if day == end_of_month:
        print(f"Next Date: {year}-{month + 1:02d}-01")
        return

    next_day = day + 1

    print(f"Next Date: {year}-{month:02d}-{next_day:02d}")


if __name__ == "__main__":
    main()
