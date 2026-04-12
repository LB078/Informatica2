from datetime import date as Date


class Transaction:
    id: int
    date: Date
    description: str
    category: str
    amount: float

    def __init__(self, id, date, description, category, amount) -> None:
        self.id = id
        self.date = date
        self.description = description
        self.category = category
        self.amount = float(amount)

    def __repr__(self):
        return f"Transaction({self.id}, '{self.date}', '{self.description}', '{self.category}', {self.amount})"
