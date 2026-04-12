import os
import sys
from databasemanager import DatabaseManager
from salesreporter import SalesReporter
from salesmanager import SalesManager


if __name__ == "__main__":
    databasemanager: DatabaseManager = DatabaseManager(
        os.path.join(sys.path[0], "sales_app.db"))
    databasemanager.restore_from_json('backup.json')

    salesreporter: SalesReporter = SalesReporter(databasemanager)
    salesmanager: SalesManager = SalesManager(databasemanager)

    print("Sales Amount:")
    print(salesreporter.sales_amount(), "\n")
    print("Total Sales:")
    print(salesreporter.total_sales(), "\n")
    print("Sales by Product:")
    print(salesreporter.sales_by_product(), "\n")
    print("Sales by Customer:")
    print(salesreporter.sales_by_customer(), "\n")
    print("Sales Over Time:")
    print(salesreporter.sales_over_time(), "\n")
    print("Top Selling Products:")
    print(salesreporter.top_selling_products(), "\n")
    print("Top Customers:")
    print(salesreporter.top_customers(), "\n")

    # Create + Update + Delete Customer
    customer_id = salesmanager.add_customer(
        'New Customer', 'newcustomer@example.com')
    assert customer_id > 0
    assert salesmanager.update_customer(
        customer_id, 'Jane Doe', 'jane@doe.com')

    print(salesmanager.get_customer(customer_id))

    assert salesmanager.get_customer(customer_id) == (
        customer_id, 'Jane Doe', 'jane@doe.com')
    assert salesmanager.delete_customer(customer_id)
    assert not salesmanager.get_customer(customer_id)

    # Create + Update + Delete Product
    product_id = salesmanager.add_product('New Product', 'Category X')
    assert product_id > 0
    assert salesmanager.update_product(product_id, 'Basecamp Gear', 'Climbing')
    assert salesmanager.get_product(product_id) == (
        product_id, 'Basecamp Gear', 'Climbing')
    assert salesmanager.delete_product(product_id)
    assert not salesmanager.get_product(product_id)

    # Create + Update + Delete Sale
    sale_id = salesmanager.add_sale('2022-02-02', 1, 1, 1, 100)
    assert sale_id > 0
    assert salesmanager.update_sale(
        sale_id, '2024-02-01', product_id, customer_id, 5, 9.99)
    assert salesmanager.get_sale(sale_id)[1] == '2024-02-01'
    assert salesmanager.get_sale(sale_id)[4] == 5
    assert salesmanager.delete_sale(sale_id)
    assert not salesmanager.get_sale(sale_id)

    databasemanager.close()
