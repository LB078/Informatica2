import json
import os
import sqlite3
import sys


class DatabaseManager:
    connection: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __init__(self, database: str) -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def fetchone(self, query: str, parameters: tuple | list | dict = ()) -> tuple:
        self.cursor.execute(query, parameters)
        return self.cursor.fetchone()

    def fetchall(self, query: str, parameters: tuple | list | dict = ()) -> list:
        self.cursor.execute(query, parameters)

        return self.cursor.fetchall()

    def insert(self, query: str, parameters: tuple | list | dict) -> int:
        self.cursor.execute(query, parameters)
        self.connection.commit()

        return self.cursor.lastrowid

    def update(self, query: str, parameters: tuple | list | dict = ()) -> bool:
        self.cursor.execute(query, parameters)
        self.connection.commit()

        return self.cursor.rowcount > 0

    def delete(self, query: str, parameters: tuple | list | dict = ()) -> bool:
        self.cursor.execute(query, parameters)
        self.connection.commit()

        return self.cursor.rowcount > 0

    def close(self):
        self.connection.close()

    def backup_to_json(self, filename: str) -> None:
        # Grab all tablenames from current database
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")

        # Setup backup dict for storage
        backup: dict = dict()

        # Loop over each table in the database
        for table in self.cur.fetchall():
            table_name: str = table[0]

            # Grab data from current table
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows: list = self.cursor.fetchall()

            # Grab table information (row + type) from table
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns: list = [(column[1], column[2], column[4], column[5])
                             for column in self.cursor.fetchall()]

            # Store info on current table
            backup[table_name] = {"columns": columns, "rows": rows}

        # Write backup to json file
        with open(os.path.join(sys.path[0], filename), 'W', encoding='utf-8') as file:
            json.dump(backup, file, indent=4)

    def restore_from_json(self, filename: str) -> None:
        # Load backup from json file
        with open(os.path.join(sys.path[0], filename), 'r', encoding='utf-8') as file:
            backup = json.load(file)

        # Recover each table one by one
        for table_name, table_data in backup.items():
            columns: list = table_data["columns"]
            rows: list = table_data["rows"]

            # Create table based on table definition if it does not exist yet
            definitions: str = ", ".join([
                f"{column[0]} {column[1]}" +
                (f" DEFAULT {column[2]}" if column[2] is not None else "") +
                (" PRIMARY KEY" if column[3] else "") +
                (" AUTOINCREMENT" if column[3]
                 and column[1].upper() == "INTEGER" else "")
                for column in columns])
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {
                                table_name} ({definitions})""")

            # Deleting any data in this table
            self.cursor.execute(f"DELETE FROM {table_name}")

            # Insert the backup data into the table
            for row in rows:
                placeholders: str = ", ".join(
                    [f":{column[0]}" for column in columns])
                insert_query: str = f"INSERT INTO {table_name} ({', '.join(
                    [col[0] for col in columns])}) VALUES ({placeholders})"
                self.cursor.execute(
                    insert_query, {column[0]: value for column, value in zip(columns, row)})

        self.connection.commit()

    def __del__(self):
        self.close()
