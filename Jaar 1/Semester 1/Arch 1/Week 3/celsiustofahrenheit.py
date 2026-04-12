# (9/5)(40) + 32

# Write a program that displays a temperature conversion table for degrees Celsius and degrees Fahrenheit.

# Criteria:
# The table should include rows for all temperatures between 0 and 100 degrees Celsius that are multiples of 10 degrees Celsius.
# Include appropriate headings on your columns.
# The formula for converting between degrees Celsius and degrees Fahrenheit can be found on the internet .
# Input example:
# No input is given

# Output example:
# °C °F
# 10 50
# 20 68


def main():
    conversions = []

    for celsius in range(0, 100, 10):
        fahrenheit = (celsius * 9 / 5) + 32

        conversions.append({"celsius": celsius, "fahrenheit": fahrenheit})

    for conversion in conversions:
        print(f"{conversion['celsius']:2d} {round(conversion['fahrenheit'])}")


if __name__ == "__main__":
    main()
