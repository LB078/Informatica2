from datetime import datetime

from contestant import Contestant
from database_handler import DatabaseHandler
from fish import Fish


unit_calculations = {
    "Gram": 1,
    "Kilogram": 1000,
    "Pound": 453.592,
    "Ounce": 28.3495,
    "Viss": 1600,
    "Stone": 6350.29,
}

local_units = {
    "DEFAULT": ["Gram", "Kilogram"],
    "US": ["Pound", "Ounce"],
    "LR": ["Pound", "Ounce"],
    "MM": ["Viss", "Ounce"],
    "CA": ["Pound", "Ounce"],
    "GB": ["Stone", "Pound"],
    "AU": ["Pound", "Ounce"],
    "BS": ["Pound", "Ounce"],
    "FJ": ["Pound", "Ounce"],
    "JM": ["Pound", "Ounce"],
    "PG": ["Pound", "Ounce"],
    "TO": ["Pound", "Ounce"],
    "IN": ["Pound", "Kilogram"],
    "KH": ["Pound", "Kilogram"],
    "TZ": ["Pound", "Kilogram"],
    "PH": ["Pound", "Kilogram"],
    "LK": ["Pound", "Kilogram"],
}


class Catch:
    database_handler: DatabaseHandler
    id: int
    fish: int
    contestant: str
    caught_at: datetime
    latitude: float
    longitude: float
    country_code: str
    weight: float
    length: float

    def __init__(
        self,
        id: int,
        fish: int,
        contestant: int,
        caught_at: datetime,
        latitude: float,
        longitude: float,
        country_code: str,
        weight: float,
        length: float,
    ) -> None:
        self.database_handler = DatabaseHandler()
        self.id = id
        self.fish = fish
        self.contestant = contestant
        self.caught_at = caught_at
        self.latitude = latitude
        self.longitude = longitude
        self.country_code = country_code
        self.weight = weight
        self.length = length

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                [
                    f"{key}={value!s}"
                    for key, value in self.__dict__.items()
                    if key != "database_handler"
                ]
            ),
        )

    def get_contestant(self) -> Contestant:
        contestant = self.database_handler.get_one(
            "Contestants",
            select=["id", "first_name", "last_name", "classification", "date_of_birth"],
            where=[("id", "=", self.id)],
        )

        return Contestant(*contestant)

    def get_fish(self) -> Fish:
        fish = self.database_handler.get_one(
            "Fishes",
            ["taxon_key", "species", "scientific_name", "kingdom"],
            where=[("taxon_key", "=", self.fish)],
        )

        return Fish(*fish)

    def get_weight_in_local_units(self) -> str:
        units = local_units.get(self.country_code, local_units["DEFAULT"])

        return ", ".join(
            [
                f"{int((self.weight / unit_calculations.get(unit, 1)) *100)/100:.2f} {unit}"
                for unit in units
            ]
        )

    def get_day_part(self) -> str:
        caught_at_hour = self.caught_at.time().hour

        if 0 <= caught_at_hour < 6:
            return "Night"
        if 6 <= caught_at_hour < 12:
            return "Morning"
        if 12 <= caught_at_hour < 18:
            return "Afternoon"
        if 18 <= caught_at_hour < 24:
            return "Evening"

    def get_season(self) -> str:
        caught_at_month = self.caught_at.date().month

        if caught_at_month in [3, 4, 5]:
            return "Spring"
        if caught_at_month in [6, 7, 8]:
            return "Summer"
        if caught_at_month in [9, 10, 11]:
            return "Autumn"
        if caught_at_month in [12, 1, 2]:
            return "Winter"

    def get_weight_category(self) -> str:
        expected_weight = 0.0123 * pow(self.length, 3.1)

        percentage = abs((expected_weight - self.weight) / expected_weight * 100)

        if percentage < 2:
            return "average"

        if self.weight < expected_weight:
            return "light"

        if self.weight > expected_weight:
            return "heavy"
