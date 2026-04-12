from datetime import date
from catch import Catch
from database_handler import DatabaseHandler
from fish import Fish
from contestant import Contestant
import os
import sys
import csv

catch_columns = [
    "id",
    "fish_id",
    "contestant_id",
    "caught_at",
    "latitude",
    "longitude",
    "country_code",
    "weight",
    "length",
]


class Reporter:
    database_handler: DatabaseHandler

    def __init__(self):
        self.database_handler = DatabaseHandler()

    def _export_csv(self, file_name, headers, data):
        try:
            with open(os.path.join(sys.path[0], file_name), "w") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
        except FileExistsError:
            print("File doesnt exist")
        except PermissionError:
            print("No permission to write file")

    def total_amount_of_fish(self) -> int:
        """
        Returns the total number of fish recorded in the database.
        """
        return self.database_handler.get_one("Fishes", ["COUNT(taxon_key)"])[0]

    def biggest_catch(self) -> Catch:
        """
        Returns the catch with the highest weight recorded in the database.
        """
        return Catch(
            *self.database_handler.get_one(
                "Catches",
                select=catch_columns,
                extra_clauses=["ORDER BY weight DESC", "LIMIT 1"],
            )
        )

    def longest_and_shortest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the longest and shortest catches recorded in the database.
        """
        longest_length = self.database_handler.get_one(
            "Catches",
            select=catch_columns,
            extra_clauses=["ORDER BY length DESC", "LIMIT 1"],
        )

        shortest_length = self.database_handler.get_one(
            "Catches",
            select=catch_columns,
            extra_clauses=["ORDER BY length ASC", "LIMIT 1"],
        )

        return (Catch(*longest_length), Catch(*shortest_length))

    def heaviest_and_lightest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the heaviest and lightest catches by weight recorded in the database.
        """
        heaviest_catch = self.database_handler.get_one(
            "Catches",
            select=catch_columns,
            extra_clauses=["ORDER BY weight DESC", "LIMIT 1"],
        )

        lightest_catch = self.database_handler.get_one(
            "Catches",
            select=catch_columns,
            extra_clauses=["ORDER BY weight ASC", "LIMIT 1"],
        )

        return (Catch(*heaviest_catch), Catch(*lightest_catch))

    def contestant_with_most_catches(self) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the most catches recorded in the database.
        """
        query_result = list(
            self.database_handler.get_one(
                table="Contestants",
                select=[
                    "Contestants.id",
                    "first_name",
                    "last_name",
                    "classification",
                    "date_of_birth",
                    "COUNT(Catches.id) as catch_amount",
                ],
                joins=[
                    "INNER JOIN Catches ON Contestants.id = Catches.contestant_id",
                ],
                extra_clauses=[
                    "GROUP BY Contestants.id",
                    "ORDER BY catch_amount DESC",
                    "LIMIT 1",
                ],
            )
        )

        query_result.pop()
        return (Contestant(*query_result),)

    def fish_with_most_catches(self) -> tuple[Fish, ...]:
        """
        Returns a tuple containing the fish species with the most catches recorded in the database.
        """
        query_result = list(
            self.database_handler.get_one(
                table="Fishes",
                select=[
                    "taxon_key",
                    "species",
                    "scientific_name",
                    "kingdom",
                    "COUNT(Catches.id) as catch_amount",
                ],
                joins=[
                    "INNER JOIN Catches ON Fishes.taxon_key = Catches.fish_id",
                ],
                extra_clauses=[
                    "GROUP BY taxon_key",
                    "ORDER BY catch_amount DESC",
                    "LIMIT 1",
                ],
            )
        )

        query_result.pop()
        return (Fish(*query_result),)

    def contestant_with_first_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the first catch of a specified fish type.
        """
        query_result = self.database_handler.get_one(
            table="Fishes",
            select=[
                "Contestants.id",
                "Contestants.first_name",
                "Contestants.last_name",
                "Contestants.classification",
                "Contestants.date_of_birth",
                "Fishes.taxon_key",
                "Catches.contestant_id",
                "Catches.caught_at",
            ],
            where=[("Fishes.species", "=", species)],
            joins=[
                "INNER JOIN Catches ON Fishes.taxon_key = Catches.fish_id",
                "INNER JOIN Contestants on Catches.contestant_id = Contestants.id",
            ],
            extra_clauses=[
                "ORDER BY Catches.caught_at ASC",
                "LIMIT 1",
            ],
        )

        if not query_result:
            return

        query_result = list(query_result)

        return (Contestant(*query_result[0:5]),)

    def contestant_with_last_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the last catch of a specified fish type.
        """
        query_result = self.database_handler.get_one(
            table="Fishes",
            select=[
                "Contestants.id",
                "Contestants.first_name",
                "Contestants.last_name",
                "Contestants.classification",
                "Contestants.date_of_birth",
                "Fishes.taxon_key",
                "Catches.contestant_id",
                "Catches.caught_at",
            ],
            where=[("Fishes.species", "=", species)],
            joins=[
                "INNER JOIN Catches ON Fishes.taxon_key = Catches.fish_id",
                "INNER JOIN Contestants on Catches.contestant_id = Contestants.id",
            ],
            extra_clauses=[
                "ORDER BY Catches.caught_at DESC",
                "LIMIT 1",
            ],
        )

        if not query_result:
            return

        query_result = list(query_result)

        return (Contestant(*query_result[0:5]),)

    def contestants_fished_between(
        self, fish: Fish, start: date, end: date, to_csv: bool = False
    ) -> tuple[Contestant, ...]:
        """
        If to_csv is False, returns a tuple containing the contestants who fished a specified fish species between two dates.
        If to_csv is True, the results are written to a CSV file.
        """
        query_result = self.database_handler.get_many(
            table="Fishes",
            select=[
                "Contestants.id",
                "Contestants.first_name",
                "Contestants.last_name",
                "Contestants.classification",
                "Contestants.date_of_birth",
                "Fishes.taxon_key",
                "Catches.contestant_id",
                "Catches.caught_at",
            ],
            where=[
                ("Fishes.species", "=", fish.species),
                ("Catches.caught_at", "BETWEEN", (start, end)),
            ],
            joins=[
                "INNER JOIN Catches ON Fishes.taxon_key = Catches.fish_id",
                "INNER JOIN Contestants on Catches.contestant_id = Contestants.id",
            ],
            extra_clauses=[
                "GROUP BY Contestants.id",
            ],
        )

        if to_csv:
            name = f"Contestant fishing between {start} and {end}.csv"
            self._export_csv(
                name,
                ("id", "first_name", "last_name", "date_of_birth", "classification"),
                [[row[0], row[1], row[2], row[4], row[3]] for row in query_result],
            )
        else:
            return tuple([Contestant(*row[0:5]) for row in query_result])

    def fish_caught_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Fish, ...]:
        """
        If to_csv is False, returns a tuple containing the fish species caught in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        query_result = self.database_handler.get_many(
            table="Catches",
            select=[
                "Fishes.taxon_key",
                "Fishes.species",
                "Fishes.scientific_name",
                "Fishes.kingdom",
                "Catches.country_code",
            ],
            where=[("Catches.country_code", "=", country_code)],
            joins=[
                "INNER JOIN Fishes ON Catches.fish_id = Fishes.taxon_key",
            ],
            extra_clauses=["GROUP BY Fishes.taxon_key"],
        )

        if to_csv:
            name = f"Fishes in country {country_code}.csv"
            self._export_csv(
                name,
                ("taxon_key", "species", "kingdom", "scientific_name"),
                [[row[0], row[1], row[3], row[2]] for row in query_result],
            )
        else:
            return tuple([Fish(*row[0:4]) for row in query_result])

    def contestants_fished_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Contestant, ...]:
        """
        If to_csv is False, returns a tuple containing the contestants who fished in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        query_result = self.database_handler.get_many(
            table="Catches",
            select=[
                "Contestants.id",
                "Contestants.first_name",
                "Contestants.last_name",
                "Contestants.classification",
                "Contestants.date_of_birth",
                "Catches.country_code",
            ],
            where=[("Catches.country_code", "=", country_code)],
            joins=[
                "INNER JOIN Contestants ON Catches.contestant_id = Contestants.id",
            ],
            extra_clauses=["GROUP BY Contestants.id"],
        )

        if to_csv:
            name = f"Contestants fished in country {country_code}.csv"
            self._export_csv(
                name,
                ("id", "first_name", "last_name", "date_of_birth", "classification"),
                [[row[0], row[1], row[2], row[4], row[3]] for row in query_result],
            )
        else:
            return tuple([Contestant(*row[0:5]) for row in query_result])
