""" Create connection and perform complex operations in database by call abbreviate methods from class instance """
import dotenv
from tkinter import messagebox
from os import getenv
from psycopg2 import connect
from uuid import uuid4

# load environment variables while module is imported each time
dotenv.load_dotenv()

# PostgreSQL database connection and operations are nested into class instance and initializated by using created prior class instance 
class DatabaseInteractions:    
    # Create connection by default with postgreSQL database
    def __init__(self) -> None:
        # Get login and database data for connection
        config = {
            "dbname": getenv("PSQL_DBNAME"),
            "user": getenv("PSQL_USER"),
            "password": getenv("PSQL_PASSWORD")
        }
        
        # Establosh connection and assign connection object to class property
        self.ac = connect(**config)

    # Add new item to database
    def add_new_item(self, item_name) -> None:
        # Execute SQL Query
        with self.ac.cursor() as cursor:
            # Plan query
            QUERY = """INSERT INTO shop_items (item_name, id) VALUES (%s, %s)"""
            cursor.execute(QUERY, (item_name, uuid4().hex,))

            # Send planned query to database
            self.ac.commit()

            # Display information that item has been added to shop inventory
            messagebox.showinfo("Success", "Item has been added to shop inventory!")

    # Get all items from database and return Array with it name's (1st tuple valie) and id's (2nd value from tuple)
    def get_items(self) -> tuple[list[str], list[str]]:
        # Ready list with obtained items name's and id's
        ready_output = ([], []) # 1st = name's list, 2nd = id's list
        
        # Execute SQL Query
        with self.ac.cursor() as cursor:
            # Plan Query
            QUERY_OBTAIN_NAMES = """SELECT item_name, id FROM shop_items"""
            cursor.execute(QUERY_OBTAIN_NAMES)

            # Execute query by send it to database
            item_names = cursor.fetchall()

            # Obtain name and id from returend by database library output and put these results to returning list with names and ids
            for name_tuple in item_names:
                # Append name
                ready_output[0].append(name_tuple[0])

                # Append id
                ready_output[1].append(name_tuple[1])

        # Return obtained item names and ids or empty list for each subsequent id and name list        
        return ready_output
    
    # Delete specified shop item by its id. Item after pass existing id will be delete from shop inventory items database
    def delete_item(self, item_id: str):
        # Execute SQL Query
        with self.ac.cursor() as cursor:
            # Plan Query
            QUERY_DELETE_SPECIFIC_ELEMENT = """DELETE FROM shop_items WHERE id=%s"""
            cursor.execute(QUERY_DELETE_SPECIFIC_ELEMENT, (item_id,))

            # Execute query by send it to database
            self.ac.commit()
            