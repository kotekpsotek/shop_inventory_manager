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