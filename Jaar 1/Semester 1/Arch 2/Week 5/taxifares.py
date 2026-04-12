# When you take a taxi to a certain place, you pay for the amount of distance you traveled along with a basefare. Write a program that interacts with the user and calculates the fare of a taxi drive for a specified distance.

# Criteria:
# Base fare is 4.00 EUR
# Fare per 140 meter traveled is 0.25 EUR
# Use a function called calculate_fare(distance)
# that takes the distance in kilometers and returns the total fare as result
# Input examples:
# Distance traveled: 2
# Distance traveled: 1.4
# Output examples:
# Total fare: 7.75 EUR
# Total fare: 6.50 EUR

def calculate_fare(distance_in_km: float) -> float:
    BASE_FARE = 4.00
    FARE_PER_140_METER = 0.25

    distance_in_m = distance_in_km * 1000

    distance_in_140_m = round(distance_in_m / 140) + \
        round(distance_in_m % 140 > 0)

    return format(BASE_FARE + (distance_in_140_m * FARE_PER_140_METER), ".2f")


def main():
    distance_in_km = float(input("Distance traveled (KM): "))
    print(f"Total fare: {calculate_fare(distance_in_km)} EUR")


if __name__ == "__main__":
    main()
