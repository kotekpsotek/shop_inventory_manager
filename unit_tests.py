""" Unit-Tests suite for whole application """
import unittest
from database import DatabaseInteractions

class Tests(unittest.TestCase):
    # Test whether connection with database can be established
    def test_database_connection(self):
        instance = DatabaseInteractions()

    # Obtain names of items from shop inventory database
    def test_database_get_names(self):
        # Obtain and get item names
        item_names = DatabaseInteractions().get_items()

        # Print result to stdout
        print(item_names)

    # Test whether function to delete items from database works correctly
    def test_database_delete_item(self):
        delete_item_db_operation = DatabaseInteractions().delete_item("1")
        pass

    # Test whether database function "get_user_password" return password of user which exist
    def test_get_user_from_database(self):
        user_password = DatabaseInteractions().get_user_password("abcd")
        print(user_password)