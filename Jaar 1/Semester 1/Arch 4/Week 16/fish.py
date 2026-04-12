from database_handler import DatabaseHandler


class Fish:
    database_handler: DatabaseHandler
    taxon_key: str
    species: str
    scientific_name: str
    kingdom: str

    def __init__(
        self, taxon_key: str, species: str, scientific_name: str, kingdom: str
    ):
        self.database_handler = DatabaseHandler()
        self.taxon_key = taxon_key
        self.species = species
        self.scientific_name = scientific_name
        self.kingdom = kingdom

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

    def get_catches(self):
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
            where=[("fish_id", "=", self.taxon_key)],
        )

        return catches
        # return (Catch(*result) for result in catches)
