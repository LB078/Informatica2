# Write a program that reads a month and day from the user.
# If the month and day match one of the Dutch national holidays then your program should display the holiday’s name.
# Otherwise your program should indicate that the entered month and day do not correspond to a fixed-date holiday.

# Criteria:
# Input is given as a comma seperated string: Month: 12, Day: 5
# If no holiday is found, print error message: No holiday found on given input
# Input example:
# Date: Month: 12, Day: 5

# Output example:
# Sinterklaas

holidays = {
    "1": {
        "1": "New Year's Day",
    },
    "2": {},
    "3": {},
    "4": {
        "27": "King's Day",
    },
    "5": {
        "5": "Liberation Day",
    },
    "6": {},
    "7": {},
    "8": {},
    "9": {},
    "10": {},
    "11": {},
    "12": {
        "5": "Sinterklaas",
        "25": "Christmas Day",
        "26": "Second Christmas Day",
    },
}


def main():
    date = input("Date: ").replace("Month: ", "").replace("Day: ", "")

    month, day = date.split(", ")

    if not month in holidays:
        print("None")
        return

    if not day in holidays[month]:
        print("None")
        return

    print(holidays[month][day])


if __name__ == "__main__":
    main()
