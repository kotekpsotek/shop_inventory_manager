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