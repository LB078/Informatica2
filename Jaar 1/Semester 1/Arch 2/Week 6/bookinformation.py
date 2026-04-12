library = list()


def book_title_exists(title: str) -> bool:
    return next((book_title for book_title in library if book_title.get(
        "title") == title), False)


def search_book(books: list[dict[str, str]], term: str) -> str:
    for book in books:
        if book.get("title").lower() == term:
            return True

        if book.get("author").lower() == term:
            return True

        if book.get("publisher").lower() == term:
            return True

        if book.get("pub_date").lower() == term:
            return True

    return False


def add_book() -> None:
    book_details = input("Book details? ")

    title, author, publisher, publish_date = book_details.split(",")

    if book_title_exists(title):
        print("Book already exists")
        return

    book_dictionary = {
        "title": title,
        "author": author,
        "publisher": publisher,
        "pub_date": publish_date
    }

    library.append(book_dictionary)
    print("Added book")


def get_book():
    search_term = input("Term? ")

    if search_book(library, search_term):
        print("Found")


def exit_program() -> None:
    for book in library:
        print(book)


menu = [
    {
        "key": "a",
        "title": "Add book",
        "function": add_book
    }, {
        "key": "s",
        "title": "Search book",
        "function": get_book
    }, {
        "key": "e",
        "title": "Exit (And print)",
        "function": exit_program,
        "exit": True
    }
]


def main():
    while True:
        for menu_item in menu:
            print(f"[{menu_item.get('key').upper()}] {menu_item.get('title')}")

        menu_choice = input("-> ").lower()

        choice = next((menu_item for menu_item in menu if menu_item.get(
            "key") == menu_choice), None)
        # https://stackoverflow.com/questions/8653516/search-a-list-of-dictionaries-in-python

        if choice is not None:
            choice.get("function")()

            # I'd use sys.exit but codegrade doesnt allow me to import the sys module
            if choice.get("exit"):
                break


if __name__ == "__main__":
    main()
