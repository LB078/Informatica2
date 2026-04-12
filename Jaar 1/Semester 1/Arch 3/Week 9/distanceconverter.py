# Calculating distances in difference formats is hard, so we would like a program to do this for us.

# Write a class called Converter.

# Criteria:
# The user will pass a length and a unit when declaring an object from the class—for example, c = Converter(9,'inches').
# For each of these units there should be a method that returns the length converted into those units. For example, using the Converter object created above, the user could call c.feet() and should get 0.75 as the result.
# Use meters as base unit to convert to and from (this prevents rounding errors)
# Units:
# inches
# feet
# yards
# miles
# kilometers
# meters
# centimeters
# millimeters
# Input example:
# c = Converter(9,'inches')
# print(c.feet())
# Output example:
# 0.75


class Converter:
    distance_in_meters: int
    unit: str

    def __init__(self, distance: int, unit: str) -> None:
        match unit:
            case "inches":
                self.distance_in_meters = distance * 0.0254
            case "feet":
                self.distance_in_meters = distance * 0.3048
            case "yards":
                self.distance_in_meters = distance * 0.9144
            case "miles":
                self.distance_in_meters = distance * 1609.344
            case "kilometers":
                self.distance_in_meters = distance * 1000
            case "meters":
                self.distance_in_meters = distance
            case "centimeters":
                self.distance_in_meters = distance * 0.01
            case "millimeters":
                self.distance_in_meters = distance * 0.001
            case _:
                raise ValueError("Invalid unit")

    def inches(self) -> float:
        return self.distance_in_meters / 0.0254

    def feet(self) -> float:
        return self.distance_in_meters / 0.3048

    def yards(self) -> float:
        return self.distance_in_meters / 0.9144

    def miles(self) -> float:
        return self.distance_in_meters / 1609.344

    def kilometers(self) -> float:
        return self.distance_in_meters / 1000

    def meters(self) -> float:
        return self.distance_in_meters

    def centimeters(self) -> float:
        return self.distance_in_meters / 0.01

    def millimeters(self) -> float:
        return self.distance_in_meters / 0.001
