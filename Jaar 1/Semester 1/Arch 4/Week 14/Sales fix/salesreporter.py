from databasemanager import DatabaseManager


class SalesReporter:
    db: DatabaseManager

    def __init__(self, databasemanager: DatabaseManager) -> None:
        self.db = databasemanager

    def sales_amount(self) -> int:
        sale = self.db.fetchone("""
        SELECT COUNT(id) from sales
        """)

        if not sale:
            return None

        return sale[0]

    def total_sales(self) -> float:
        return self.db.fetchone("""
        SELECT ROUND(SUM(quantity * price),2) from sales
        """)[0]

    def sales_by_product(self) -> str:
        sales = self.db.fetchall("""
        SELECT name, SUM(quantity), ROUND(SUM(quantity * price),2) FROM sales
        INNER JOIN products ON sales.product_id = products.id
        GROUP BY products.id
        """)

        return self.display_table(["Product", "Quantity", "Sales"], sales)

    def sales_by_customer(self) -> str:
        sales = self.db.fetchall("""
        SELECT name, SUM(quantity), ROUND(SUM(quantity * price),2) FROM sales
        INNER JOIN customers ON sales.customer_id = customers.id
        GROUP BY customers.id
        """)

        return self.display_table(["Customer", "Quantity", "Sales"], sales)

    def sales_over_time(self) -> str:
        sales = self.db.fetchall("""
        SELECT date, ROUND(SUM(quantity * price),2) FROM sales
        GROUP BY date
        """)

        return self.display_table(["Date", "Sales"], sales)

    def top_selling_products(self, amount: int = 5) -> str:
        sales = self.db.fetchall("""
        SELECT name, SUM(quantity) as productQuantity FROM sales
        INNER JOIN products ON sales.product_id = products.id
        GROUP BY products.id
        ORDER BY productQuantity DESC
        LIMIT ?
        """, (amount,))

        return self.display_table(["Product", "Quantity"], sales)

    def top_customers(self, amount: int = 5) -> str:
        sales = self.db.fetchall("""
        SELECT name, ROUND(SUM(quantity * price),2) as salePrice FROM sales
        INNER JOIN customers ON sales.customer_id = customers.id
        GROUP BY name
        ORDER BY salePrice DESC, name ASC
        LIMIT ?
        """, (amount,))

        return self.display_table(["Customer", "Sales"], sales)

    def display_table(self, headers: list[str], rows: list[tuple]) -> str:
        """
        Formats and displays a list of rows as a table with headers.

        Parameters:
        headers (list of str): The column headers of the table.
        rows (list of tuple): The data rows to be displayed in the table. Each tuple represents a row of data.

        Returns:
        str: A string representation of the table formatted for display.

        Example:
        >>> headers = ["Product", "Total Quantity", "Total Sales"]
        >>> rows = [("Product A", 100, 999.99), ("Product B", 150, 1499.99), ("Product C", 200, 1999.99)]
        >>> reporter = SalesReporter('sales.db')
        >>> table_str = reporter.display_table(headers, rows)
        >>> print(table_str)

        Example Output:
        Product   | Total Quantity | Total Sales
        ---------+----------------+------------
        Product A | 100            | 999.99
        Product B | 150            | 1499.99
        Product C | 200            | 1999.99
        """
        column_widths: list = [max(len(str(item)) for item in column)
                               for column in zip(*([headers] + rows))]
        row_format: str = " | ".join(
            ["{{:<{}}}".format(width) for width in column_widths])
        table: list = list()

        table.append(row_format.format(*headers))
        table.append("-+-".join(['-' * width for width in column_widths]))

        for row in rows:
            table.append(row_format.format(*row))

        return "\n".join(table)
