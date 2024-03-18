"""
Module containing functions related to database setup.
"""
import os
import sqlite3

DATABASE_PATH = "/data/devices.db"

# Ensure the parent directory of the database file exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


def setup_database(db_name=DATABASE_PATH):
    """
    Sets up the device management database.

    This function creates two tables: 'coordinates' and 'devices'.
    - The 'coordinates' table stores latitude and longitude values.
    - The 'devices' table stores device information, including UUID, deployment date, and owner.

    Parameters:
    - db_name (str): The name of the SQLite database file. Default is '/data/devices.db'.
    """
    with sqlite3.connect(db_name) as database:
        cursor = database.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coordinates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                device_uuid TEXT PRIMARY KEY,
                localisation_id INTEGER,
                deployment_date TEXT,
                owner TEXT NOT NULL,
                FOREIGN KEY (localisation_id) REFERENCES coordinates(id)
            )
        ''')
        database.commit()
