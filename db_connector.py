import sqlite3
from sqlite3 import Error
from config import DB_PATH

class Connector(object):
    def __init__(self, path):
        self.path = path

    def _create_connection(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect(self.path)
        except Error as e:
            print(f"Error '{e}' occurred.")
        return self.connection

    def execute(self, query):
        connection = self._create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
            except Error as e:
                result = None
                print(f"Error {e} occurred.")
            connection.close()
            return result
        else: 
            return None

    def execute_many(self, query, data):
        connection = self._create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.executemany(query, data)
                result = cursor.fetchall()
                connection.commit()
            except Error as e:
                result = None
                print(f"Error {e} occurred.")
            connection.close()
            return result
        else: 
            return None

connector = Connector(DB_PATH)