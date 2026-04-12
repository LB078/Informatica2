import os
import sqlite3
import sys


class DatabaseHandler:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        self.cursor = self.connection.cursor()

    def _get(
        self,
        table: str,
        select: list[str],
        where: list[tuple[str, str, str | int | None]] = None,
        joins: list[str] = None,
        extra_clauses=None,
    ):
        if not where:
            where = list()

        select = ", ".join(select)
        where_clause = "AND ".join(
            [
                f"""{column[0]} {column[1]}
                {f":{column[0].replace('.', '')}{index}_1 AND :{column[0].replace('.', '')}{index}_2"
                    if isinstance(column[2], tuple) else
                    f":{column[0].replace('.', '')}{index}"}
                """
                for index, column in enumerate(where)
            ]
        )

        query = f"""
            SELECT {select}
            FROM {table} {f' '.join(joins) if joins else ''}
            {f'WHERE {where_clause}' if where else ''}
            {f' '.join(extra_clauses) if extra_clauses else ''}
        """

        values = {}

        for index, value in enumerate(where):
            if isinstance(value[2], tuple):
                values[f"{value[0].replace('.', '')}{index}_1"] = value[2][0]
                values[f"{value[0].replace('.', '')}{index}_2"] = value[2][1]
            else:
                values[f"{value[0].replace('.', '')}{index}"] = value[2]

        self.cursor.execute(query, values)

    def get_one(
        self,
        table: str,
        select: list[str],
        where: list[tuple[str, str, str | int | None]] = None,
        joins: list[str] = None,
        extra_clauses: list[str] = None,
    ):
        self._get(table, select, where, joins, extra_clauses)

        return self.cursor.fetchone()

    def get_many(
        self,
        table: str,
        select: list[str],
        where: list[tuple[str, str, str | int | None]] = None,
        joins: list[str] = None,
        extra_clauses: list[str] = None,
    ):
        self._get(table, select, where, joins, extra_clauses)

        return self.cursor.fetchall()

    def insert(self, table: str, columns: list[str], values: list[str]) -> int | None:
        columns = ", ".join(columns)

        query = f"""
            INSERT INTO {table} ({columns}) VALUES ({','.join(["?" for _ in values])})
        """

        self.cursor.execute(query, values)
        return self.cursor.lastrowid

    def commit(self) -> None:
        self.connection.commit()
