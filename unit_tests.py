""" Unit-Tests suite for whole application """
import unittest
from database import DatabaseInteractions

class Tests(unittest.TestCase):
    def test_database_connection(self):
        instance = DatabaseInteractions()
