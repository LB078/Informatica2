import os
import sys
import json
import sqlite3

from datetime import datetime
from transaction import Transaction


class FinanceApp:
    def __init__(self, db_name="finance.db"):
        self.connection = sqlite3.connect(os.path.join(sys.path[0], db_name))
        self.cursor = self.connection.cursor()

    def build_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS transactions")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            description TEXT,
                            category TEXT,
                            amount REAL)"""
        )
        self.connection.commit()

    def load_transactions_from_json(self, json_file):
        with open(os.path.join(sys.path[0], json_file), "r", encoding="utf-8") as file:
            json_data = json.load(file)

            for transaction in json_data:
                self.add_transaction(
                    datetime.strptime(transaction["date"], "%d-%m-%Y").strftime(
                        "%Y-%m-%d"
                    ),
                    transaction["description"],
                    transaction["category"],
                    transaction["amount"],
                )

    def add_transaction(self, date, description, category, amount) -> Transaction:
        self.cursor.execute(
            "INSERT INTO transactions (date, description, category, amount) VALUES (?, ?, ?, ?)",
            (date, description, category, amount),
        )
        self.connection.commit()

        return Transaction(self.cursor.lastrowid, date, description, category, amount)

    def update_transaction(
        self, transaction_id, date, description, category, amount
    ) -> bool:
        update_fields = []
        update_values = []

        if date:
            update_fields.append("date = ?")
            update_values.append(date)
        if description:
            update_fields.append("description = ?")
            update_values.append(description)
        if category:
            update_fields.append("category = ?")
            update_values.append(category)
        if amount is not None:
            update_fields.append("amount = ?")
            update_values.append(amount)

        update_values.append(transaction_id)

        self.cursor.execute(
            f"UPDATE transactions SET {', '.join(update_fields)} WHERE id = ?",
            update_values,
        )
        self.connection.commit()

        return self.cursor.rowcount > 0

    def delete_transaction(self, transaction_id) -> bool:
        self.cursor.execute(
            "DELETE FROM transactions WHERE id = ?", (transaction_id,))
        self.connection.commit()

        return self.cursor.rowcount > 0

    def search_transactions(self, term: str) -> list[Transaction]:
        self.cursor.execute(
            """SELECT id, date, description, category, amount FROM transactions
            WHERE description LIKE ? OR category LIKE ?""",
            (f"%{term}%", f"%{term}%"),
        )

        return [Transaction(*row) for row in self.cursor.fetchall()]

    def get_transactions(self, year: int | None = None) -> list[Transaction]:
        if year:
            self.cursor.execute(
                "SELECT id, date, description, category, amount FROM transactions WHERE date LIKE ?",
                (f"{year}%",),
            )
        else:
            self.cursor.execute(
                "SELECT id, date, description, category, amount FROM transactions"
            )

        return [Transaction(*row) for row in self.cursor.fetchall()]

    def get_expenses(self) -> list[tuple[str, float]]:
        self.cursor.execute(
            """
            SELECT category, ROUND(SUM(amount),2) as amount_sum
            FROM transactions WHERE (NOT amount > 0 AND NOT category = 'Work') OR category = 'Savings'
            GROUP BY category
            ORDER BY amount_sum DESC"""
        )

        return self.cursor.fetchall()

    def get_savings(self) -> list[tuple[str, float]]:
        self.cursor.execute(
            """
            SELECT STRFTIME('%Y',date) as year, ABS(ROUND(SUM(amount),2)) as amount_sum
            FROM transactions WHERE category = 'Savings'
            GROUP BY year
            ORDER BY year ASC"""
        )

        return self.cursor.fetchall()

    def count_transactions(self, year: int | None = None) -> int:
        if year:
            self.cursor.execute(
                "SELECT COUNT(id) FROM transactions WHERE STRFTIME('%Y',date) = ?",
                (year,),
            )
        else:
            self.cursor.execute("SELECT COUNT(id) FROM transactions")

        return self.cursor.fetchone()[0]

    def get_report(self, year: int | None = None) -> dict[str, float]:
        query = """SELECT COUNT(id), ROUND(SUM( ),2) as income_sum,
            ROUND(SUM(
                CASE WHEN (amount < 0 AND category NOT IN ('Work', 'Savings')) THEN amount ELSE 0 END
            ),2) as expenses_sum,
            ABS(ROUND(SUM(CASE WHEN category = 'Savings' THEN amount ELSE 0 END),2)) as savings_sum
            FROM transactions"""

        if year:
            query += "\nWHERE STRFTIME('%Y',date) = ?"
            self.cursor.execute(query, (year,))
        else:
            self.cursor.execute(query)

        query_result = self.cursor.fetchone()

        return {
            "transactions": query_result[0],
            "income": query_result[1],
            "expenses": query_result[2],
            "savings": query_result[3],
            "total": round(query_result[1] + query_result[2] + query_result[3], 2),
        }
