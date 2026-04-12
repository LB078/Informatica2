# The following data represents average temperatures of the third month for 1995, 2010, and 2020 recorded in Amsterdam.

# Dataset:
# temperatures = (
#     ('1995', '3', ['47.3', '40.0', '38.3', '36.3', '37.4', '40.3', '41.1', '40.5', '41.6', '43.2', '46.2', '45.8', '44.9', '39.4', '40.5',
#      '42.0', '46.5', '46.2', '43.3', '41.7', '40.7', '39.6', '44.2', '47.8', '45.9', '47.3', '39.8', '35.2', '38.5', '40.5', '47.0']),
#     ('2010', '3', ['39.2', '36.7', '35.5', '35.2', '35.8', '33.8', '30.7', '33.2', '32.3', '33.3', '37.3', '39.9', '40.8', '42.9', '42.7',
#      '42.6', '44.8', '50.3', '52.2', '55.2', '47.2', '45.0', '48.6', '55.0', '57.4', '50.9', '48.6', '46.2', '49.6', '50.1', '43.6']),
#     ('2020', '3', ['43.2', '41.1', '40.0', '43.6', '42.6', '44.0', '44.0', '47.9', '46.6', '50.5', '51.5', '47.7', '44.7', '44.0', '48.9',
#      '45.3', '46.6', '49.7', '47.2', '44.8', '41.8', '40.9', '41.0', '42.7', '43.4', '44.0', '46.4', '45.5', '40.7', '39.5', '40.6'])
# )
# Criteria:
# Implement a program that given this data prints the answers for the following questions (each seperate line):

# How many different values occur as a daily average temperature in both March 1995 and March 2010.
# How many different values occur as a daily average temperature in both March 1995 and March 2020.
# Which year has a day with highest temperature in March?
# Which year had the warmest March?
# Input example:
# No input is given

# Output example:
# Answer_1
# Answer_2
# Answer_3
# Answer_4

temperatures = (
    ('1995', '3', [
        '47.3', '40.0', '38.3', '36.3', '37.4', '40.3', '41.1', '40.5', '41.6', '43.2',
        '46.2', '45.8', '44.9', '39.4', '40.5', '42.0', '46.5', '46.2', '43.3', '41.7',
        '40.7', '39.6', '44.2', '47.8', '45.9', '47.3', '39.8', '35.2', '38.5', '40.5', '47.0'
    ]),
    ('2010', '3', [
        '39.2', '36.7', '35.5', '35.2', '35.8', '33.8', '30.7', '33.2', '32.3', '33.3',
        '37.3', '39.9', '40.8', '42.9', '42.7', '42.6', '44.8', '50.3', '52.2', '55.2',
        '47.2', '45.0', '48.6', '55.0', '57.4', '50.9', '48.6', '46.2', '49.6', '50.1', '43.6'
    ]),
    ('2020', '3', [
        '43.2', '41.1', '40.0', '43.6', '42.6', '44.0', '44.0', '47.9', '46.6', '50.5',
        '51.5', '47.7', '44.7', '44.0', '48.9', '45.3', '46.6', '49.7', '47.2', '44.8',
        '41.8', '40.9', '41.0', '42.7', '43.4', '44.0', '46.4', '45.5', '40.7', '39.5', '40.6'
    ])
)


def main():
    march_1995_temperatures = temperatures[0]
    march_2010_temperatures = temperatures[1]
    march_2020_temperatures = temperatures[2]

    march_1995_temperatures_set = set(march_1995_temperatures[2])
    march_2010_temperatures_set = set(march_2010_temperatures[2])
    march_2020_temperatures_set = set(march_2020_temperatures[2])

    common_1995_2010 = march_1995_temperatures_set & march_2010_temperatures_set
    common_1995_2020 = march_1995_temperatures_set & march_2020_temperatures_set

    print(len(common_1995_2010))
    print(len(common_1995_2020))
    # Warmest temperature in march year

    max_temperature_year = None
    max_temperature_highest_temperature = None
    for year in temperatures:
        max_temperature = max(year[2])

        if max_temperature_highest_temperature is None or max_temperature > max_temperature_highest_temperature:
            max_temperature_year = year[0]
            max_temperature_highest_temperature = max_temperature

    print(max_temperature_year)

    # Warmest average temperature

    highest_average_year = None
    highest_average_temperature = None
    for year in temperatures:
        average_temperature = sum(float(temperature)
                                  for temperature in year[2]) / len(year[2])

        if highest_average_temperature is None or average_temperature > highest_average_temperature:
            highest_average_year = year[0]
            highest_average_temperature = average_temperature

    print(highest_average_year)


if __name__ == "__main__":
    main()
