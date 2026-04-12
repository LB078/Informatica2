import os
import sys
import csv


def load_csv_file(file_name):
    file_content = []

    with open(os.path.join(sys.path[0], file_name), newline='', encoding="utf8") as csv_file:
        file_content = list(csv.DictReader(csv_file, delimiter=","))

    return file_content


def get_headers(file_content: list[dict[str, str]]) -> list[str]:
    return file_content[0].keys()


def search_by_type(file_content: list[dict[str, str]], show_type: str) -> list[dict[str, str]]:
    return list(
        filter(lambda x: x["type"] == show_type, file_content))


def search_by_director(file_content: list[dict[str, str]], director: str) -> list[dict[str, str]]:
    return list(
        filter(lambda x: director == x["director"], file_content))


def get_directors(file_content: list[dict[str, str]]) -> set[str]:
    return {item["director"] for item in file_content if item["director"]}


def main():
    print("[1] Print the amount of TV Shows")
    print("[2] Print the amount of Movies")
    print("[3] Print the (full) names of directors in alphabetical order who lead both tv shows and movies.")
    print("""[4] Print the name of each director in alphabetical order,
          the number of movies and the number of tv shows (s)he was the director of.""")

    menu_choice = input("Enter your choice: ")
    if menu_choice not in ["1", "2", "3", "4"]:
        print("Invalid input")
        return

    netflix_titles = load_csv_file("netflix_titles.csv")

    match menu_choice:
        case "1":
            print(len(search_by_type(netflix_titles, "TV Show")))
        case "2":
            print(len(search_by_type(netflix_titles, "Movie")))
        case "3":
            all_directors = get_directors(netflix_titles)

            filtered_directors = list()

            for director in all_directors:
                movies_of_director = search_by_director(
                    netflix_titles, director)

                if (len(search_by_type(movies_of_director, "Movie")) > 0 and
                        len(search_by_type(movies_of_director, "TV Show")) > 0):
                    filtered_directors.append(director)

            print(sorted(filtered_directors))
        case "4":
            all_directors = get_directors(netflix_titles)

            director_stats = list()

            for director in sorted(all_directors):
                movies_of_director = search_by_director(
                    netflix_titles, director)

                movies = len(search_by_type(movies_of_director, "Movie"))
                tv_shows = len(search_by_type(movies_of_director, "TV Show"))

                director_stats.append((director, movies, tv_shows))

            print(director_stats)


if __name__ == "__main__":
    main()
