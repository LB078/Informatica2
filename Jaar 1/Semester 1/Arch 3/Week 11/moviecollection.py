import os
import sys
import json


class MovieArchive:
    movies: list[dict[str, str | int | list[str]]]
    movie_archive_filepath: str

    def __init__(self, movie_archive_filepath) -> None:
        self.movie_archive_filepath = movie_archive_filepath
        self.movies = self._read()

    def _read(self) -> list[dict[str, str | int | list[str]]]:
        with open(os.path.join(sys.path[0], self.movie_archive_filepath), encoding="utf-8") as file:
            return json.load(file)

    def _save(self) -> bool:
        with open(os.path.join(sys.path[0], self.movie_archive_filepath), "w", encoding="utf-8") as file:
            json.dump(self.movies, file)
            return True

    def search(
            self,
            title: str = None,
            min_year: int = None,
            max_year: int = None,
            cast: list[str] = None,
            genres: list[str] = None
    ) -> list[dict[str, str | int | list[str]]]:
        def search_filter(movie):
            if title:
                if title.lower() not in movie["title"].lower():
                    return False

            if min_year:
                if movie["year"] < min_year:
                    return False

            if max_year:
                if movie["year"] > max_year:
                    return False

            if cast:
                if not any(actor in movie["cast"] for actor in cast):
                    return False

            if genres:
                if not any(genre in movie["genres"] for genre in genres):
                    return False

            return True

        return list(filter(search_filter, self.movies))

    def edit(
        self,
        target_title: str,
        new_title: str | None = None,
        new_year: int | None = None,
    ) -> bool:
        if len(self.search(target_title)) == 0:
            return False

        for movie in self.movies:
            if movie["title"].lower() == target_title.lower():
                if new_title:
                    movie["title"] = new_title
                if new_year:
                    movie["year"] = new_year

        return self._save()

    def edit_cast(self, cast_changes: dict[str, str]) -> None:
        for movie in self.movies:
            for current_actor, new_actor in cast_changes.items():
                if current_actor in movie["cast"]:
                    if new_actor is None:
                        movie["cast"].remove(current_actor)
                    else:
                        movie["cast"][movie["cast"].index(
                            current_actor)] = new_actor

        self._save()


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main() -> None:
    print("[I] Movie information overview")
    print("[M] Make modification based on assignment")
    print("[S] Search a movie title ")
    print("[C] Change title and/or release year by search on title")
    print("[Q] Quit program")

    movie_archive = MovieArchive('movies.json')

    while True:
        menu_choice = get_input("Menu choice? ",
                                lambda x: x.lower() in ["i", "m", "s", "c", "q"]).lower()

        match menu_choice:
            case "i":
                print("Amount of movies released in 2004",
                      len(movie_archive.search(min_year=2004, max_year=2004)))

                print("Amount of movies with genre 'Science Fiction'",
                      len(movie_archive.search(genres=["Science Fiction"])))

                print("All movies with actor 'Keanu Reeves'",
                      movie_archive.search(cast=["Keanu Reeves"]))

                print("All movies with actor 'Sylvester Stallone' released between 1995 and 2005.",
                      movie_archive.search(cast=["Sylvester Stallone"], min_year=1995, max_year=2005))
            case "m":
                movie_archive.edit("gladiator", new_year=2001)

                if len(movie_archive.movies) > 0:
                    oldest_movie = movie_archive.movies[0]
                    movie_archive.edit(oldest_movie.get(
                        "title"), new_year=oldest_movie.get("year") - 1)

                movie_archive.edit_cast({"Natalie Portman": "Nat Portman"})

                movie_archive.edit_cast({"Kevin Spacey": None})

            case "s":
                search_title = get_input("Title? ", lambda x: len(x) != 0)
                print(movie_archive.search(search_title))
            case "c":
                target_title = get_input(
                    "Movie title you want to change? ", lambda x: len(x) != 0)

                new_title = input("New Title? ") or None
                new_year = int(input("New release date? ") or 0) or None

                movie_archive.edit(target_title, new_title, new_year)
            case "q":
                break


if __name__ == "__main__":
    main()
