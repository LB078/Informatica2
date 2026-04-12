from moviecollection import MovieArchive
from unittest import TestCase, main
import os
import sys


class TestMovieArchive(TestCase):
    with open(os.path.join(sys.path[0], "movies.json"), "r", encoding="utf-8") as file:
        with open(os.path.join(sys.path[0], "movies_test.json"), "w", encoding="utf-8") as new_file:
            new_file.write(file.read())

    archive = MovieArchive("movies_test.json")

    def test_single_movie_search(self):
        search_result = self.archive.search(title="Ocean's Eleven")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0]["title"], "Ocean's Eleven")

    def test_multiple_movie_search(self):
        search_result = self.archive.search(
            title="Ocean's", cast=["Brad Pitt", "George Clooney"]
        )
        self.assertEqual(len(search_result), 3)

    def test_cast_search(self):
        search_result = self.archive.search(cast=["Brad Pitt"])
        self.assertEqual([movie["title"]
                         for movie in search_result].count("Ocean's Eleven"), 1)

    def test_edit_title_movie(self):
        self.archive.edit("John Wick: Chapter 2",
                          new_title="John Doe: Chapter 2")
        search_result = self.archive.search(title="John Doe: Chapter 2")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0]["title"], "John Doe: Chapter 2")

    def test_edit_year_movie(self):
        self.archive.edit("Inglourious Basterds", new_year=2022)
        search_result = self.archive.search(title="Inglourious Basterds")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0]["year"], 2022)

    def test_edit_cast(self):
        self.archive.edit_cast({"Amber Heard": None})
        search_result = self.archive.search(cast=["Amber Heard"])
        self.assertEqual(len(search_result), 0)


if __name__ == "__main__":
    main()
