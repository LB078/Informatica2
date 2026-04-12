class TemperatureDataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.temperature_data = []

    # Method to open the file and load lines as an attribute
    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = [line.strip().split() for line in file]
                self.temperature_data = [
                    list(map(int, d[:-1]))+[float(d[len(d)-1])] for d in data]
        except FileNotFoundError:
            print('File not found')
        except ValueError:
            print('[1] Invalid data in the file')

    # Method to perform the analysis and construct the list
    def construct_temperature_list(self):
        temperature_list = []
        for data in self.temperature_data:
            print(data)
            try:
                month, day, year, temperature = data[:]
                if year not in [item[0] for item in temperature_list]:
                    temperature_list.append((year, {}))
                if month not in temperature_list[-1][1]:
                    temperature_list[-1][1][month] = 0.0
                temperature_list[-1][1][month] = max(
                    temperature, temperature_list[-1][1][month])
            except ValueError as error:
                print('Invalid data in the file', error)
            except IndexError as error:
                print('Invalid data in temperature data', error)

        return temperature_list


def main():
    # File is build up of year, month, day, temperature, separated by space
    file_path = './temps.txt'
    analyzer = TemperatureDataAnalyzer(file_path)
    analyzer.load_data()
    temperature_list = analyzer.construct_temperature_list()
    # Output: [(2019, {1: 32.0, 2: 45.0, 3: 50.0}), (2020, {1: 35.0, 2: 48.0, 3: 55.0})]
    print(temperature_list)


if __name__ == '__main__':
    main()
