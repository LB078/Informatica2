# It is commonly said that one human year is equivalent to 7 dog years.
# However this simple conversion fails to recognize that dogs reach adulthood in approximately two years.
# As a result, some people believe that it is better to count each of the first two human years as 10.5 dog years, and then count each additional human year as 4 dog years.
# Write a program that implements the conversion from human years to dog years described in the previous paragraph.

# Criteria:
# First 2 human years are 10.5 dog years per human year
# Each extra human year is 4 dog years per human year
# Ensure that your program works correctly for conversions of less than two human years and for conversions of two or more human years
# Your program should display an error message Only positive numbers are allowed if the user enters a negative number
# Input examples:
# Human years: 1
# Human years: 4
# Human years: -1
# Output examples:
# Dog years: 10.5
# Dog years: 29
# Only positive numbers are allowed

FIRST_TWO_DOG_YEARS = 10.5
DOG_YEAR = 4


def is_valid_input(value):
    if value < 0:
        return False, "Only positive numbers are allowed"

    return True, ""


def main():

    years = int(input("Years: "))

    valid_input, message = is_valid_input(years)

    if not valid_input:
        print(message)
        return

    if years <= 2:
        print(f"Dog years: {years * FIRST_TWO_DOG_YEARS}")
    else:
        print(f"Dog years: {FIRST_TWO_DOG_YEARS * 2 + (years - 2) * DOG_YEAR}")


if __name__ == "__main__":
    main()
