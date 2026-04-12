from databasemanager import DatabaseManager


class SalesManager:
    db: DatabaseManager

    def __init__(self, databasemanager: DatabaseManager) -> None:
        self.db = databasemanager

    def get_sale(self, sale_id: int) -> tuple:
        return self.db.fetchone("SELECT * FROM sales WHERE id = ?", (sale_id,))

    def add_sale(self, date: str, product_id: int, customer_id: int, quantity: int, price: float) -> int:
        return self.db.insert("""
        INSERT INTO sales (date, product_id, customer_id, quantity, price) VALUES (?,?,?,?,?)
        """, (date, product_id, customer_id, quantity, price))

    def update_sale(self,
                    sale_id: int,
                    date: str,
                    product_id: int,
                    customer_id: int,
                    quantity: int,
                    price: float) -> bool:

        return self.db.update("""
        UPDATE sales SET
        date = :date,
        product_id = :product_id,
        customer_id = :customer_id,
        quantity = :quantity,
        price = :price
        WHERE id = :sale_id
        """, {
            "sale_id": sale_id,
            "date": date,
            "product_id": product_id,
            "customer_id": customer_id,
            "quantity": quantity,
            "price": price,
        })

    def delete_sale(self, sale_id: int) -> bool:
        return self.db.delete("""
        DELETE FROM sales
        WHERE id = ?
        """, (sale_id,))

    def get_customer(self, customer_id: int) -> tuple:
        return self.db.fetchone(
            "SELECT * FROM customers WHERE id = ?", (customer_id,))

    def add_customer(self, name: str, email: str) -> int:
        return self.db.insert("""
        INSERT INTO customers (name, email) VALUES (?, ?)
        """, (name, email))

    def update_customer(self, customer_id: int, name: str, email: str) -> bool:
        return self.db.update("""
        UPDATE customers SET
        name = :name,
        email = :email
        WHERE id = :customer_id
        """, {
            "customer_id": customer_id,
            "name": name,
            "email": email,
        })

    def delete_customer(self, customer_id: int) -> bool:
        return self.db.delete("DELETE FROM customers WHERE id = ?", (customer_id,))

    def get_product(self, product_id: int) -> tuple:
        return self.db.fetchone(
            "SELECT * FROM products WHERE id = ?", (product_id,))

    def add_product(self, name: str, category: str) -> int:
        return self.db.insert("""
        INSERT INTO products (name, category) VALUES (?, ?)
        """, (name, category))

    def update_product(self, product_id: int, name: str, category: str) -> bool:
        return self.db.update("""
        UPDATE products SET
        name = :name,
        category = :category
        WHERE id = :product_id
        """, {
            "product_id": product_id,
            "name": name,
            "category": category,
        })

    def delete_product(self, product_id: int) -> bool:
        return self.db.delete("DELETE FROM products WHERE id = ?", (product_id,))
