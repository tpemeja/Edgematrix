import sqlite3


def setup_database(db_name='devices.db'):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
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
        db.commit()
