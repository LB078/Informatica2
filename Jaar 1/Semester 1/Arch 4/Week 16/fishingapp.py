import json
import os
import sys
from database_handler import DatabaseHandler


def is_database_empty(database_handler: DatabaseHandler) -> bool:

    catches_length = database_handler.get_one("Catches", select=["COUNT(id)"])[0]
    contestants_length = database_handler.get_one("Contestants", select=["COUNT(id)"])[
        0
    ]
    fishes_length = database_handler.get_one("Fishes", select=["COUNT(taxon_key)"])[0]

    return sum([catches_length, contestants_length, fishes_length]) == 0


contestant_ids = list()


def create_contestant(database_handler: DatabaseHandler, contestant):
    if contestant["id"] in contestant_ids:
        return

    contestant_ids.append(contestant["id"])

    database_handler.insert(
        "Contestants",
        columns=["id", "first_name", "last_name", "classification", "date_of_birth"],
        values=[
            contestant["id"],
            contestant["first_name"],
            contestant["last_name"],
            contestant["classification"],
            contestant["date_of_birth"],
        ],
    )


fish_ids = list()


def create_fish(database_handler: DatabaseHandler, fish):
    if fish["taxon_key"] in fish_ids:
        return

    fish_ids.append(fish["taxon_key"])

    database_handler.insert(
        "Fishes",
        columns=["taxon_key", "species", "kingdom", "scientific_name"],
        values=[
            fish["taxon_key"],
            fish["species"],
            fish["kingdom"],
            fish["scientific_name"],
        ],
    )


def create_catch(database_handler: DatabaseHandler, catch):

    create_contestant(database_handler, catch["candidate"])
    create_fish(database_handler, catch["fish"])

    coordinates = catch["coordinate"].split(", ")

    database_handler.insert(
        "Catches",
        columns=[
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
        values=[
            catch["id"],
            catch["fish"]["taxon_key"],
            catch["candidate"]["id"],
            catch["datetime"],
            coordinates[0],
            coordinates[1],
            catch["country_code"],
            catch["weight"],
            catch["length"],
        ],
    )


def restore_database(database_handler: DatabaseHandler, backup_file):
    with open(os.path.join(sys.path[0], backup_file)) as file:
        loaded_json = json.load(file)

        for row in loaded_json:
            create_catch(database_handler, row)

        database_handler.commit()


def main():
    database_handler = DatabaseHandler()

    if is_database_empty(database_handler):
        restore_database(database_handler, "catches.json")


if __name__ == "__main__":
    main()
