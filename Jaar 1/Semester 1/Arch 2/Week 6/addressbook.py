import os
import sys
import json


"""
print all contacts in the following format:
======================================
Position: <position>
First name: <firstname>
Last name: <lastname>
Emails: <email_1>, <email_2>
Phone numbers: <number_1>, <number_2>
"""


def display(addressbook: list[dict[str, str]]) -> None:
    for contact in addressbook:
        print(
            f"""
======================================
Position: {contact.get("id")}
First name: {contact.get("first_name")}
Last name: {contact.get("last_name")}
Emails: {", ".join(contact.get("emails"))}
Phone numbers: {", ".join(contact.get("phone_numbers"))}
              """
        )


"""
return list of contacts sorted by first_name or last_name [if blank then unsorted], direction [ASC (default)/DESC])
"""


def list_contacts(
    addressbook: list[dict[str, str]], sort: str = None, sort_direction: str = "asc"
) -> list[dict[str, str]]:
    addressbook_copy = addressbook.copy()

    if sort not in ["first_name", "last_name"]:
        sort = None

    if sort:
        if sort_direction == "asc":
            addressbook_copy.sort(key=lambda x: x[sort])
        else:
            addressbook_copy.sort(key=lambda x: x[sort], reverse=True)

    return addressbook_copy


"""
add new contact:
- first_name
- last_name
- emails = {}
- phone_numbers = {}
"""


def add_contact(
    addressbook: list[dict[str, str]],
    first_name: str,
    last_name: str,
    emails: str,
    phone_numbers: str,
) -> None:
    emails = emails.split(",")
    phone_numbers = phone_numbers.split(",")

    max_id = 0
    if len(addressbook) > 0:
        max_id = max(addressbook, key=lambda x: x["id"])["id"]

    contact_info = {
        "id": max_id + 1,
        "first_name": first_name,
        "last_name": last_name,
        "emails": emails,
        "phone_numbers": phone_numbers,
    }

    addressbook.append(contact_info)


"""
remove contact by ID (integer)
"""


def remove_contact(addressbook: list[dict[str, str]], id: str) -> None:
    contact_index = next(
        (
            index
            for index, contact in enumerate(addressbook)
            if contact.get("id") == int(id)
        ),
        None,
    )
    # based off https://stackoverflow.com/questions/8653516/search-a-list-of-dictionaries-in-python

    if contact_index is not None:
        addressbook.pop(contact_index)


"""
merge duplicates (automated > same fullname [firstname & lastname])
"""


def merge_contacts(addressbook: list[dict[str, str | list[str]]]) -> None:
    merged_contacts: list[dict[str, str | list[str]]] = []
    merged_names = []

    for contact in addressbook:
        merged_name = (
            contact.get("first_name").lower() +
            contact.get("last_name").lower()
        )
        if merged_name not in merged_names:
            merged_contacts.append(contact)
            merged_names.append(merged_name)
        else:
            existing_contact_index = merged_names.index(merged_name)

            existing_contact = merged_contacts[existing_contact_index]

            for email in contact.get("emails"):
                if email not in existing_contact.get("emails"):
                    existing_contact["emails"].append(email)

            for phone_number in contact.get("phone_numbers"):
                if phone_number not in existing_contact.get("phone_numbers"):
                    existing_contact["phone_numbers"].append(phone_number)

    addressbook = merged_contacts


"""
read_from_json
Do NOT change this function
"""


def read_from_json(filename) -> list:
    addressbook = list()
    # read file
    with open(os.path.join(sys.path[0], filename)) as outfile:
        json_data = json.load(outfile)
        # iterate over each line in data and call the add function
        for contact in json_data:
            addressbook.append(contact)

    return addressbook


"""
write_to_json
Do NOT change this function
"""


def write_to_json(filename, addressbook: list) -> None:
    json_object = json.dumps(addressbook, indent=4)

    with open(os.path.join(sys.path[0], filename), "w") as outfile:
        outfile.write(json_object)


"""
main function:
# build menu structure as following
# the input can be case-insensitive (so E and e are valid inputs)
# [L] List contacts
# [A] Add contact
# [R] Remove contact
# [M] Merge contacts
# [Q] Quit program
Don't forget to put the contacts.json file in the same location as this file!
"""

character_set = set("abcdefghijklmnopqrstuvwxyz")


def is_valid_name(name):
    name_set = set(name.lower())

    if len(name_set.difference(character_set)) == 0:
        return True

    return False


def get_input(prompt: str, validation_function) -> str:
    while True:
        input_value = input(prompt)
        if validation_function(input_value):
            return input_value
        else:
            print("Input error")


def main(json_file):
    addressbook = read_from_json(json_file)
    while True:

        print(
            """
[L] List contacts
[A] Add contact
[R] Remove contact
[M] Merge contacts
[Q] Quit program
            """
        )

        choice = get_input(
            "Pick option: ", lambda x: x.lower() in ["l", "a", "r", "m", "q"]
        ).lower()

        if choice == "l":
            sorted_adressbook = list_contacts(addressbook)
            display(sorted_adressbook)
        elif choice == "a":
            first_name = get_input("First name? ", is_valid_name)
            last_name = get_input("Last name? ", is_valid_name)
            emails = get_input(
                "E-mails? ", lambda x: all(
                    ["@" in email for email in x.split(",")])
            )
            phone_numbers = get_input(
                "Phone numbers? ",
                lambda x: all(
                    [phone_number.isdigit() for phone_number in x.split(",")]
                ),
            )

            add_contact(addressbook, first_name,
                        last_name, emails, phone_numbers)
            print("Contact added to addressbook")
        elif choice == "r":
            id_input = get_input("Id to remove? ", lambda x: x.isdigit())

            remove_contact(addressbook, id_input)
        elif choice == "m":
            merge_contacts(addressbook)
        elif choice == "q":
            break

        write_to_json(json_file, addressbook)


if __name__ == "__main__":
    main("contacts.json")
