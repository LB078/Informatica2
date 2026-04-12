# Create an application for a car dealer.

# The problem is split up into three steps to help you set up a proper structure for the application.

# Step 1 - Create a class name Car:
# Criteria:
# Create four fields (brand, model, color, price) and implement these using the init function.
# Create a fifth field called sold. The default value for sold is False.
# Create a method called sell that changes the value of sold to True.
# Create a method called print that prints all fields in a comprehensible way (see example).
# Output example (print):
# Brand: BMW
# Model: X5
# Color: Black
# Price: 34.899
# Not sold yet

# Step 2 - Create a new class named Customer:
# Criteria:
# Give it one field (name) and properly implement it.
# Create a method print that returns all fields in a comprehensible way (see example).
# Modify the Car class with a field sold_to, set this field to an object of Customer within the sell method
# (which now needs a parameter with a Customer object).
# Edit the print method of the Car to print the information about the customer if the car has been sold, in addition to the information that will already be printed.
# Adjust other code where needed to get everything working properly.
# Output example (print - Customer):
# Name: John Doe
# Output example (print - Car):
# Brand: BMW
# Model: X5
# Color: Black
# Price: 34.899
# Sold to: John Doe

# Step 3 - Extending business by selling motorcycles:
# Write all code to properly introduce this into the existing application.
class Customer:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def print(self):
        print(f"Name: {self.name}")

# Create vehicle abstraction class


class Vehicle:
    brand: str
    model: str
    color: str
    price: float
    sold: bool
    sold_to: Customer

    def __init__(self, brand: str, model: str, color: str, price: float) -> None:
        self.brand = brand
        self.model = model
        self.color = color
        self.price = float(str(price).replace(".", "").replace(",", "."))
        self.sold = False

    def sell(self, customer: Customer) -> None:
        self.sold = True
        self.sold_to = customer

    def print(self):
        print(f'''Brand: {self.brand}, Model: {self.model}, Color: {self.color}, Price: {
            self.price:.2f}, Sold: {f"Sold to {self.sold_to.name}" if self.sold else "Not sold yet"}''')


class Motorcycle(Vehicle):
    pass


class Car(Vehicle):
    pass


if __name__ == "__main__":
    car = Car("AUDI", "A3", "BLUE", 19.999)
    car.print()
