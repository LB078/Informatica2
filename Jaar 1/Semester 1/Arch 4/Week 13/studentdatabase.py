import os
import sys
import sqlite3
import datetime


class StudentHandler:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.connection = sqlite3.connect(
            os.path.join(sys.path[0], 'studentdatabase.db'))
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS students (
                studentnumber INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                city TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                class TEXT DEFAULT NULL
            );'''
        )
        self.connection.commit()

    def add_student(self, first_name, last_name, city, date_of_birth, class_name: str = None) -> int:
        query = "INSERT INTO students (first_name, last_name, city, date_of_birth, class) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(query, (first_name, last_name,
                            city, date_of_birth, class_name if class_name else None))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_students(self, student_number: int = None, class_name: str = None) -> list[tuple]:
        query = "SELECT * FROM students"

        query_parameters = []

        if student_number:
            query += " WHERE studentnumber = ?"
            query_parameters.append(student_number)

        if class_name:
            if "WHERE" in query:
                query += " AND class = ?"
            else:
                query += " WHERE class = ?"

            query_parameters.append(class_name)

        query += " ORDER BY class DESC"

        self.cursor.execute(query, query_parameters)

        return self.cursor.fetchall()

    def search_student(self, search_term: str) -> tuple:
        search_term = f"%{search_term}%"
        query = """SELECT * FROM students
        WHERE first_name LIKE :search_term OR last_name LIKE :search_term OR city LIKE :search_term
        """

        self.cursor.execute(query, {"search_term": search_term})

        return self.cursor.fetchone()

    def assign_student(self, student_number: int, class_name: str) -> bool:
        if not self.get_students(student_number=student_number):
            return False

        query = "UPDATE students SET class = ? WHERE studentnumber = ?;"
        self.cursor.execute(query, (class_name, student_number))
        self.connection.commit()
        return self.cursor.rowcount > 0


def validate_date(date: str) -> bool:
    date = list(map(int, date.split("-")))

    if not 1 <= date[0] <= 31:
        print("Day")
        return False

    if not 1 <= date[1] <= 12:
        print("Month")
        return False

    if not 1900 <= date[2] <= datetime.datetime.now().year:
        print("Year")
        return False

    return True


def format_date(date: str) -> str:
    date = date.split("-")
    return "-".join((date[2], date[1], date[0]))


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main():
    print("[A] Add new student")
    print("[C] Assign student to class")
    print("[D] List all students")
    print("[L] List all students in class")
    print("[S] Search student")
    print("[Q] Quit program")

    student_handler = StudentHandler()

    while True:
        menu_choice = get_input("Enter your choice: ", lambda x: x.lower() in (
                                "a", "c", "d", "l", "s", "q")).lower()

        match menu_choice:
            case "a":
                first_name = get_input("First name: ", lambda x: len(x) > 1)
                last_name = get_input("Last name: ", lambda x: len(x) > 1)
                city = get_input("City: ", lambda x: len(x) > 1)
                date_of_birth = get_input("Date of birth: ", validate_date)
                class_name = get_input(
                    "Class (leave empty if none): ", lambda x: x)

                print(student_handler.add_student(first_name,
                      last_name, city, date_of_birth, class_name))
            case "c":
                student_number = get_input(
                    "Student number: ", lambda x: x)

                if len(student_handler.get_students(student_number=int(student_number))) == 0:
                    print(f"""Could not find student with number:
                          {student_number}""")
                    return

                class_name = get_input("Class: ", lambda x: len(x) > 1)

                student_handler.assign_student(student_number, class_name)
            case "d":
                for student in student_handler.get_students():
                    print(student)
            case "l":
                class_name = get_input("Class: ", lambda x: len(x) > 1)
                for student in student_handler.get_students(class_name=class_name):
                    print(student)
            case "s":
                search_term = get_input("Search term: ", lambda x: len(x) > 1)

                search_result = student_handler.search_student(search_term)

                print(search_result)
            case "q":
                break


if __name__ == "__main__":
    main()
