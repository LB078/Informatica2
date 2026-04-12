import os
import sys


month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


# that given the value in fahrenheit returns the temperature in celsius (rounding is not needed)
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


# that calculates the average temperature per month. Return a list of tuples (month, temperature).
def average_temp_per_month(temperatures_for_year: dict[str, list[str]]) -> list[tuple]:

    average_temperature_list = list()

    for month, temperatures in temperatures_for_year.items():
        average_temperature = sum(map(float, temperatures)) / len(temperatures)

        average_temperature_list.append((month, average_temperature))

    return average_temperature_list


# that calculates the average temperature per year. Return a list of tuples (year, temperature).
def average_temp_per_year(temperatures: dict[str, dict[str, list[str]]]) -> list[tuple]:
    average_temperature_list = list()
    for year, months in temperatures.items():
        total_temperature = 0
        amount_of_temperatures = 0

        for temperatures in months.values():
            total_temperature += sum(temperatures)
            amount_of_temperatures += len(temperatures)

        average_temperature_list.append(
            (int(year), total_temperature / amount_of_temperatures))

    return average_temperature_list


def file_to_dict(file: list) -> dict[int, dict[int, list[int]]]:
    weather_dict = dict()

    for row in file:
        month, year, temperature = int(row[0]), int(row[2]), float(row[3])

        if not weather_dict.get(year):
            weather_dict[year] = dict()

        if not weather_dict[year].get(month):
            weather_dict[year][month] = list()

        weather_dict[year][month].append(temperature)

    return weather_dict


def load_txt_file(file_name):
    file_content = []

    with open(
        os.path.join(sys.path[0], file_name), newline="", encoding="utf8"
    ) as file_obj:
        for line in file_obj.readlines():
            file_content.append(line.split())

    return file_content


def get_input(
    prompt: str,
    validation_function=None,
    input_error: str = "Input error",
    repeat_on_error: bool = True,
) -> str | None:
    while True:
        input_value = input(prompt)

        if validation_function is not None:
            if not validation_function(input_value):
                print(input_error)
                if not repeat_on_error:
                    return None
                continue

        return input_value


def main():
    file = load_txt_file("NLAMSTDM.txt")
    weather_dict = file_to_dict(file)

    print(
        """
[1] Print the average temperatures per year (fahrenheit)
[2] Print the average temperatures per year (celsius) Hint: Use built-in map() function.
[3] Print the warmest and coldest year as tuple based on the average temperature
[4] Print the warmest month of a year based on the input year of the user (full month name)
[5] Print the coldest month of a year based on the input year of the user (full month name)
[6] Print a list of tuples where the first element of each tuple is the
year and the second element of the tuple is a dictionary with months as
the keys and the average temperature (in Celsius) of each month as the value
          """
    )

    menu_choice = get_input("Option? ", lambda x: x in [
                            "1", "2", "3", "4", "5", "6"])

    match menu_choice:
        case "1":
            print(average_temp_per_year(weather_dict))
        case "2":
            print(list(map(lambda x: (x[0], fahrenheit_to_celsius(
                x[1])), average_temp_per_year(weather_dict))))
        case "3":
            average_temps = average_temp_per_year(weather_dict)
            warmest_year = max(average_temps, key=lambda x: x[1])
            coldest_year = min(average_temps, key=lambda x: x[1])
            print((warmest_year[0], coldest_year[0]))
        case "4":
            year = int(get_input("Year? ", lambda x: int(x)
                       in weather_dict.keys()))

            max_temp = max(average_temp_per_month(
                weather_dict.get(year)), key=lambda x: x[1])

            print(month_dict.get(max_temp[0]))
        case "5":
            year = int(get_input("Year? ", lambda x: int(x)
                       in weather_dict.keys()))

            min_temp = min(average_temp_per_month(
                weather_dict.get(year)), key=lambda x: x[1])

            print(month_dict.get(min_temp[0]))
        case "6":
            print([
                (
                    year,
                    {
                        month: fahrenheit_to_celsius(average_temp)
                        for month, average_temp in average_temp_per_month(temperature)
                    }
                )
                for year, temperature in weather_dict.items()
            ])


if __name__ == "__main__":
    main()
