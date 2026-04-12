from datetime import date, datetime
from database_handler import DatabaseHandler


class Contestant:
    database_handler: DatabaseHandler
    id: str
    first_name: str
    last_name: str
    classification: str
    date_of_birth: date

    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        classification: str,
        date_of_birth: datetime,
    ):
        self.database_handler = DatabaseHandler()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.classification = classification
        self.date_of_birth = datetime.strptime(str(date_of_birth), "%Y-%m-%d").date()

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

    def get_age(self, at_date: date = date.today()) -> int:
        return (at_date.year - self.date_of_birth.year) - (
            (at_date.month, at_date.day)
            < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def get_catches(self) -> tuple:
        catches = self.database_handler.get_many(
            "Catches",
            select=[
                "id",
                "fish_id",
                "contestant_id",
                "caught_at",
                "latitude",
                "longitude",
                "country_code",
                "weight",
                "length",
            ],
            where=[("contestant_id", "=", self.id)],
        )

        return catches
        # return (Catch(*result) for result in catches)
