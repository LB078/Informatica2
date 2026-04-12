import os
import sys
import json
import sqlite3
from datetime import date, datetime, timedelta


def dict_factory(cursor, row):
    row_dict = {}
    for idx, col in enumerate(cursor.description):
        row_dict[col[0]] = row[idx]
    return row_dict


class BookstoreDatabaseManager:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    fine_per_day = 0.5

    def __init__(self):
        self.connection = sqlite3.connect(
            os.path.join(sys.path[0], 'bookstore.db'))
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            year TEXT NOT NULL,
            status TEXT DEFAULT "AVAILABLE",
            return_date DATE DEFAULT NULL
        );'''
        )
        self.connection.commit()
        self.restore_from_local_database()

    def restore_from_local_database(self):
        with open(os.path.join(sys.path[0], 'books.json')) as books_json:
            for book in json.load(books_json):
                if not self.search_book_by_id_or_isbn(book["isbn"]):
                    self.create_book(book)

    def create_book(self, book: dict) -> int:
        query = """INSERT INTO books (isbn, title, author, pages,year)
        VALUES (:isbn, :title, :author, :pages,:year)"""

        self.cursor.execute(query, book)
        self.connection.commit()

        return self.cursor.lastrowid

    def search_book_by_id_or_isbn(self, search_id, fields="*"):
        query = f"""SELECT {",".join(fields)} FROM books
        WHERE isbn = :search_id OR ID = :search_id"""

        self.cursor.execute(query, {
            "search_id": search_id
        })

        return self.cursor.fetchone()

    def update_book(self, book_id, fields, values) -> bool:
        set_clause = ", ".join([f"{field} = ?" for field in fields])

        query = f"""
            UPDATE books
            SET {set_clause}
            WHERE id = ? OR isbn = ?
        """  # error zit op de plek dat geen isbn (duh)
        # self.connection.set_trace_callback(print)

        self.cursor.execute(query, values + [book_id, book_id])
        self.connection.commit()
        # self.connection.set_trace_callback(None)

        return self.cursor.rowcount > 0

    def borrow_book(self, search_id: str, duration: int) -> str:
        book = self.search_book_by_id_or_isbn(search_id, fields=["status"])

        if book["status"] == "BORROWED":
            return False

        return_date = (date.today() + timedelta(days=int(duration))
                       ).strftime("%d-%m-%Y")

        update_succes = self.update_book(search_id, ["status", "return_date"], [
                                         "BORROWED", return_date])

        if update_succes:
            return return_date
        else:
            False

    def return_book(self, search_id: str) -> int:
        book = self.search_book_by_id_or_isbn(
            search_id, fields=["status", "return_date"])

        if book["status"] == "AVAILABLE":
            return False

        return_date = date.today()
        book_return_date = datetime.strptime(
            book["return_date"], "%d-%m-%Y").date()

        days_too_late = (return_date - book_return_date).days

        # print(days_too_late)
        fine = max(0, days_too_late * self.fine_per_day)

        self.update_book(search_id, ["status", "return_date"], [
            "AVAILABLE", None])

        return fine

    def find_book(self, search_term: str) -> list[dict]:
        query = """
        SELECT *
        FROM books
        WHERE title = :search OR isbn = :search OR author = :search
        """

        self.cursor.execute(query, {"search": search_term})

        return self.cursor.fetchall()


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main():
    print("[B] Borrow book")
    print("[R] Return book")
    print("[S] Search book")
    print("[Q] Quit program")

    bookstore_database_manager = BookstoreDatabaseManager()

    while True:
        menu_choice = get_input("Menu choice: ", lambda x: x.lower() in [
                                "b", "r", "s", "q"]).lower()

        match menu_choice:
            case "b":
                book_id = get_input(
                    "Book ID or isbn: ", lambda x: len(x) > 0)

                duration = get_input("Duration: ", lambda x: int(x) > 0)

                borrow_success = bookstore_database_manager.borrow_book(
                    book_id, duration)

                if borrow_success:
                    print(f"""Successfully borrowed book:{
                          book_id} until {borrow_success} days.""")
            case "r":
                book_id = get_input(
                    "Book ID or isbn: ", lambda x: bookstore_database_manager.search_book_by_id_or_isbn(x))

                fine = bookstore_database_manager.return_book(book_id)

                if fine:
                    print(f"{fine:.2f}")
            case "s":
                search_term = get_input(
                    "Search term: ", lambda x: len(x) > 0)

                found_books = bookstore_database_manager.find_book(search_term)

                for book in found_books:
                    print(book)

            case "q":
                break


if __name__ == "__main__":
    main()
