import os
import sys
import csv


def ensure_consistent_keys(csv_data: list[dict[str, str]], fieldnames: list[str]) -> list[dict[str, str]]:
    for item in csv_data:
        for key in list(item.keys()):
            if key not in fieldnames:
                del item[key]
    return csv_data


def load_csv_file(file_name) -> list[dict[str, str]]:
    file_content = []

    with open(os.path.join(sys.path[0], file_name), newline='', encoding="utf8") as csv_file:
        file_content = list(csv.DictReader(csv_file, delimiter=","))

    return file_content


def save_csv_file(file_name, data: list[dict[str, str]]) -> None:
    fieldnames = ["Id", "Game", "Series", "Country", "Details", "Ban Category", "Ban Status",
                  "Wikipedia Profile", "Image", "Summary", "Developer", "Publisher", "Genre", "Homepage"]
    csv_data = ensure_consistent_keys(data, fieldnames)
    with open(os.path.join(sys.path[0], file_name), "w", newline='', encoding="utf8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)


def search_games(
    games: list[dict[str, str]],
    name: str = None,
    country: str = None,
) -> list[dict[str, str | int | list[str]]]:
    def search_filter(game):

        if name:
            if name.lower() not in game["Game"].lower():
                return False

        if country:
            if country.lower() not in game["Country"].lower():
                return False

        return True

    return list(filter(search_filter, games))


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main(filename: str) -> None:
    print("[I] Print request info from assignment")
    print("[M] Make modification based on assignment")
    print("[A] Add new game to list")
    print("[O] Overview of banned games per country")
    print("[S] Search the dataset by country")
    print("[Q] Quit program")

    games = load_csv_file(filename)

    while True:
        menu_choice = get_input("Enter your choice: ", lambda x: x.lower() in [
                                "i", "m", "a", "o", "s", "q"]).lower()

        match menu_choice:
            case "i":
                # How many games got banned in Israel?
                print(len(search_games(games, country="isreal")))

                # Which country got the most games banned?
                games_per_country = {}
                for game in games:
                    if game["Country"] not in games_per_country:
                        games_per_country[game["Country"]] = 0

                    games_per_country[game["Country"]] += 1

                print(max(games_per_country, key=games_per_country.get))

                # How many games within the Assassin's Creed series are currently banned?
                print(len({game['Game']
                      for game in search_games(games, name="Assasins Creed")}))

                # Show all games (and the details) banned in Germany.
                for game in search_games(games, country="germany"):
                    print(f"{game['Game']}, {game['Details']}")

                # Show all countries (and the details) the game Red Dead Redemption got banned in.
                for game in search_games(games, name="Red Dead Redemption"):
                    print(f"{game['Country']}, {game['Details']}")
            case "m":
                games = [game for game in games if game["Country"].lower()
                         != "germany"]
                save_csv_file(filename, games)

                for game in games:
                    if game["Game"] == "Silent Hill VI":
                        game["Game"] = "Silent Hill Remastered"

                save_csv_file(filename, games)

                for game in games:
                    if game["Game"] == "Bully" and game["Country"].lower() == "brazil":
                        game["Ban Status"] = "Ban Lifted"
                save_csv_file(filename, games)

                for game in games:
                    if game["Game"] == "Manhunt II":
                        game["Genre"] = "Action"
                save_csv_file(filename, games)
            case "a":
                new_game = {
                    "Id": get_input("Enter game id: ", lambda x: len(x) > 0),
                    "Game": get_input("Enter game name: ", lambda x: len(x) > 0),
                    "Series": get_input("Enter game series: ", lambda x: len(x) > 0),
                    "Country": get_input("Enter country: ", lambda x: len(x) > 0),
                    "Details": get_input("Enter details: ", lambda x: len(x) > 0),
                    "Ban Category": get_input("Enter ban category: ", lambda x: len(x) > 0),
                    "Ban Status": get_input("Enter ban status: ", lambda x: len(x) > 0),
                    "Wikipedia Profile": get_input("Enter wikipedia profile: ", lambda x: len(x) > 0),
                    "Image": get_input("Enter image: ", lambda x: len(x) > 0),
                    "Summary": get_input("Enter summary: ", lambda x: len(x) > 0),
                    "Developer": get_input("Enter developer: ", lambda x: len(x) > 0),
                    "Publisher": get_input("Enter publisher: ", lambda x: len(x) > 0),
                    "Genre": get_input("Enter genre: ", lambda x: len(x) > 0),
                    "Homepage": get_input("Enter homepage: ", lambda x: len(x) > 0),
                }

                games.append(new_game)
                save_csv_file(filename, games)
            case "o":
                countries = sorted({game["Country"] for game in games})

                for country in countries:
                    games_per_country = search_games(games, country=country)
                    print(f"{country} - {len(games_per_country)}")
                    for game in games_per_country:
                        print(f"- {game['Game']}")
            case "s":
                search_country = get_input(
                    "Enter country to search for: ", lambda x: len(x) > 0)

                for game in search_games(games, country=search_country):
                    print(f"{game['Game']} - {game['Details']}")
            case "q":
                break


if __name__ == "__main__":
    main("bannedvideogames.csv")
