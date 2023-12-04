import json
import sqlite3
from contextlib import contextmanager
from os.path import dirname, abspath, join

current_dir = dirname(abspath(__file__))
historical_data = join(current_dir, "weather.json")
database = join(current_dir, "weather.db")

def setup():
    # Create a connection to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Create table
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather
            (country text, city text, month text, high int, low int)
        ''')
    except sqlite3.OperationalError as e:
        if "no such table" in e.args[0]:
            cursor.execute('''
                CREATE TABLE weather
                (country text, city text, month text, high int, low int)
            ''')
        else:
            raise

# create a context manager function to handle the connection to the database
# and close it automatically when the function returns
@contextmanager
def get_connection():
    conn = sqlite3.connect(database)
    try:
        yield conn
    finally:
        conn.close() 


def populate():
    # Open the JSON file and load the data
    with open(historical_data) as f:
        data = json.load(f)
    setup()

    with get_connection() as conn:
        cursor = conn.cursor()
        # Iterate over the data and insert each record into the SQLite database
        for country, cities in data.items():
            for city, months in cities.items():
                for month, temperatures in months.items():
                    high = temperatures['high']
                    low = temperatures['low']
                    cursor.execute('''
                        INSERT INTO weather VALUES (?,?,?,?,?)
                    ''', (country, city, month, high, low))
        conn.commit()