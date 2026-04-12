from unittest import TestCase, main, TestLoader
# Opmerking: De aanpak die hier wordt laten zien, is een eenvoudige introductie in unit testen.
# Later zal je meer diepgaande technieken leren met behulp van de ingebouwde frameworks en libraries van Python

contacts = []


def add_contact(name, phone_number, email):
    contact = {
        'name': name,
        'phone_number': phone_number,
        'email': email
    }
    contacts.append(contact)


def search_by_name(name):
    return list(filter(lambda c: name.lower() in c['name'].lower(), contacts))


def delete_contact(name):
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            contacts.remove(contact)


def test():
    # Test adding a contact
    add_contact('John Doe', '06876543210', 'john@hotemail.com')
    # Let's check if the function works correctly
    if len(contacts) != 1 or contacts[0]['name'] != 'John Doe':
        print('Test: ERROR in add_contact()')

    # Test searching contacts
    search_results = search_by_name("John")
    # Let's check if the function works correctly
    if len(search_results) < 1:
        print('Test: ERROR in search_by_name()')

    # Test deleting a contact
    delete_contact("John Doe")

    deleted_search_result = search_by_name("John")

    if len(deleted_search_result) > 0:
        print("Test: ERROR in delete_contact()")

    print("All tests are executed.")


class TestContactMethods(TestCase):

    def setUp(self):
        # Clear the contacts list before each test
        contacts.clear()

    def test_add_contact(self):
        add_contact('John Doe', '06876543210', 'john@hotemail.com')
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['name'], 'John Doe')
        self.assertEqual(contacts[0]['phone_number'], '06876543210')
        self.assertEqual(contacts[0]['email'], 'john@hotemail.com')

    def test_search_by_name(self):
        add_contact('John Doe', '06876543210', 'john@hotemail.com')
        search_results = search_by_name('John')
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]['name'], 'John Doe')

    def test_delete_contact(self):
        add_contact('John Doe', '06876543210', 'john@hotemail.com')
        delete_contact('John Doe')
        self.assertEqual(len(contacts), 0)
        search_results = search_by_name('John')
        self.assertEqual(len(search_results), 0)

if __name__ == '__main__':
    main()
