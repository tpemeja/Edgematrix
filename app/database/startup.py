import aiosqlite


async def setup_database(db_name='devices.db'):
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS coordinates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
            ''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    device_uuid TEXT PRIMARY KEY,
                    localisation_id INTEGER,
                    deployment_date TEXT,
                    owner TEXT NOT NULL,
                    FOREIGN KEY (localisation_id) REFERENCES coordinates(id)
                )
            ''')
            await db.commit()
