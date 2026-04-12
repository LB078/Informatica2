from passwordmanager import PasswordManager
from unittest import TestCase, main


class TestPasswordManager(TestCase):
    def test_set_password(self):
        password_manager = PasswordManager()
        password_manager.set_password("password")
        self.assertEqual(password_manager.get_password(), "password")

    def test_is_correct(self):
        password_manager = PasswordManager()
        password_manager.set_password("password")
        self.assertTrue(password_manager.is_correct("password"))

    def test_is_incorrect(self):
        password_manager = PasswordManager()
        password_manager.set_password("password")
        self.assertFalse(password_manager.is_correct("incorrect_password"))

    def test_overwrite_password(self):
        password_manager = PasswordManager()
        password_manager.set_password("password")
        password_manager.set_password("new_password")
        self.assertEqual(password_manager.get_password(), "new_password")

    def test_old_passwords(self):
        password_manager = PasswordManager()
        password_manager.set_password("password")
        password_manager.set_password("new_password")
        self.assertEqual(password_manager.old_passwords,
                         ["password", "new_password"])


if __name__ == "__main__":
    main()
