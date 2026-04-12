from financeapp import FinanceApp

if __name__ == "__main__":
    app = FinanceApp()

    while True:
        print("\nFinance App Menu")
        print("A. Add Transaction")
        print("U. Update Transaction")
        print("D. Delete Transaction")
        print("G. Get Transactions")
        print("S. Search Transactions")
        print("P. Print report")
        print("R. Restore database")
        print("E. Exit")

        choice = input("Enter your choice: ").upper()

        if choice == 'A':
            date = input("Enter the date (YYYY-MM-DD): ")
            description = input("Enter the description: ")
            category = input("Enter the category: ")
            amount = float(input("Enter the amount: "))

            transaction = app.add_transaction(date, description, category, amount)

            print(f"Transaction added: \n{transaction}")

        elif choice == 'U':
            transaction_id = int(input("Enter the transaction ID to update: "))
            date = input("Enter the new date (YYYY-MM-DD): ")
            description = input("Enter the new description: ")
            category = input("Enter the new category: ")
            amount = float(input("Enter the new amount: "))

            if app.update_transaction(transaction_id, date, description, category, amount):
                print("Transaction has been updated")
            else:
                print("Error while updating transaction")

        elif choice == 'D':
            transaction_id = int(input("Enter the transaction ID to delete: "))

            if app.delete_transaction(transaction_id):
                print("Transaction has been deleted")
            else:
                print("Could not delete transaction with id", transaction)

        elif choice == 'G':
            year = input("Enter year (leave empty for all): ")

            for transaction in app.get_transactions(year):
                print(transaction)

        elif choice == 'S':
            search_term = input("Search term: ")

            for transaction in app.search_transactions(search_term):
                print(transaction)
        elif choice == 'P':
            year = input("Enter year (leave empty for all): ")

            for key, value in app.get_report(year).items():
                print(f"{key.capitalize()}: {value}")
        elif choice == 'R':
            app.build_database()
            app.load_transactions_from_json('transactions.json')

            print("Database restored")
        elif choice == 'E':
            break
        else:
            print("Invalid choice. Please try again.")
