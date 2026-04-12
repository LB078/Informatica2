# Create a solution for a shop that wants to keep track of the stock of their products and wants to give a discount to customers who buy large quantities of the product.

# Write a class called Product

# Criteria:
# The class should have attributes called name, amount, and price (holding the product’s name, the number of items of that product in stock, and the regular price of the product).
# There should be a method get_price that receives the number of items to be bought and returns the total costs.
# There should also be a method called make_purchase that receives the number of items to be bought and decreases amount by that much.
# Extra:
# Regular price if orders have less than 10 item;
# 10% discount is applied for orders of between 10 and 99 items;
# 20% discount is applied for orders of 100 items or more.
# Input example:
# No input is given

# Output example:
# No output is required


class Product:
    name: str
    amount: int
    price: float

    def __init__(self, name: str, amount: int, price: float) -> None:
        self.name = name
        self.amount = amount
        self.price = price

    def get_price(self, number_of_items: int) -> float:
        if number_of_items < 10:
            return self.price * number_of_items
        elif 10 <= number_of_items < 100:
            return (self.price * number_of_items) * 0.9
        else:
            return (self.price * number_of_items) * 0.8

    def make_purchase(self, number_of_items: int):
        self.amount -= number_of_items
