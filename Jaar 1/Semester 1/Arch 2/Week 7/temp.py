def load_txt_file(filename):
    temperatures = {}
    with open('NLAMSTDM.txt', 'r') as file:
        for line in file:
            month, day, year, temp = line.strip().split()
            month, day, year, temp = int(month), int(day), int(year), float(temp)
            if year not in temperatures:
                temperatures[year] = {}
            if month not in temperatures[year]:
                temperatures[year][month] = []
            temperatures[year][month].append(temp)
    return temperatures


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5.0 / 9.0


def average_temp_per_month(temperatures_for_year: dict) -> list:
    average_temps = []
    for month, temps in temperatures_for_year.items():
        avg_temp = sum(temps) / len(temps)
        average_temps.append((month, avg_temp))
    return average_temps


def average_temp_per_year(temperatures: dict) -> list:
    average_per_year = []
    for year, months in temperatures.items():
        total_temp = 0
        count = 0
        for month, temps in months.items():
            total_temp += sum(temps)
            count += len(temps)
            
        if count > 0:
            avg_temp = total_temp / count
            average_per_year.append((year, avg_temp))
    return average_per_year


def warmest_and_coldest_year(average_per_year: list) -> tuple:
    sorted_years = sorted(average_per_year, key=lambda x: x[1])
    coldest_year = sorted_years[0]
    warmest_year = sorted_years[-1]
    return (warmest_year, coldest_year)


def warmest_month_of_year(temperatures: dict, year: int) -> str:
    if year not in temperatures:
        return None
    months_avg = average_temp_per_month(temperatures[year])
    warmest_month = max(months_avg, key=lambda x: x[1])
    return month_name(warmest_month[0])


def coldest_month_of_year(temperatures: dict, year: int) -> str:
    if year not in temperatures:
        return None
    months_avg = average_temp_per_month(temperatures[year])
    coldest_month = min(months_avg, key=lambda x: x[1])
    return month_name(coldest_month[0])


def month_name(month_number):
    month_mapping = {
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
    return month_mapping.get(month_number, "Invalid Month")


def average_temp_per_year_dict(temperatures: dict) -> list:
    result = []
    for year, months in temperatures.items():
        month_avgs = average_temp_per_month(months)
        monthly_dict = {month_name(month): avg for month, avg in month_avgs}
        result.append((year, monthly_dict))
    return result


def main():
    filename = 'amsterdam_temperatures.txt'  # replace with your filename
    temperatures = load_txt_file(filename)

    print("[1] Print average temperatures per year (Fahrenheit)")
    print(average_temp_per_year(temperatures))

    print("[2] Print average temperatures per year (Celsius)")
    avg_farenheit = average_temp_per_year(temperatures)
    avg_celsius = [(year, fahrenheit_to_celsius(temp)) for year, temp in avg_farenheit]
    print(avg_celsius)

    print("[3] Print the warmest and coldest year as tuple based on the average temperature")
    print(warmest_and_coldest_year(avg_farenheit))

    year_input = int(input("[4] Enter the year for warmest month: "))
    warmest_month = warmest_month_of_year(temperatures, year_input)
    print(f"The warmest month in {year_input} is: {warmest_month}")

    year_input = int(input("[5] Enter the year for coldest month: "))
    coldest_month = coldest_month_of_year(temperatures, year_input)
    print(f"The coldest month in {year_input} is: {coldest_month}")

    print("[6] Print a list of tuples with yearly average temperatures per month in Celsius")
    print(average_temp_per_year_dict(temperatures))


if __name__ == "__main__":
    main()