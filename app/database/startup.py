"""
Module containing functions related to database setup.
"""

import sqlite3


def setup_database(db_name='devices.db'):
    """
    Sets up the device management database.

    This function creates two tables: 'coordinates' and 'devices'.
    - The 'coordinates' table stores latitude and longitude values.
    - The 'devices' table stores device information, including UUID, deployment date, and owner.

    Parameters:
    - db_name (str): The name of the SQLite database file. Default is 'devices.db'.
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
