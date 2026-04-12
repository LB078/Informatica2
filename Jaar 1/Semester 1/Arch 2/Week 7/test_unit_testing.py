from unittest import TestCase, main
from unit_testing import add_contact, search_by_name, delete_contact, contacts

class TestContactMethods(TestCase):

    def setUp(self):
        contacts.clear()

    def test_add_contact(self):
        add_contact('John Doe', '06123456790', 'john.doe@email.com')
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].get('name'), 'John Doe')
        self.assertEqual(contacts[0].get('phone_number'), '06123456790')
        self.assertEqual(contacts[0].get('email'), 'john.doe@email.com')

    def test_search_by_name(self):
        add_contact('Jane Doe', '06123456790', 'john.doe@email.com')
        search_results = search_by_name('Jane')
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].get('name'), 'Jane Doe')

    def test_delete_contact(self):
        add_contact('John Doe', '06123456790', 'john.doe@email.com')
        delete_contact('John Doe')
        self.assertEqual(len(contacts), 0)
        search_results = search_by_name('John')
        self.assertEqual(len(search_results), 0)

if __name__ == '__main__':
    main()