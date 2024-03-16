import aiosqlite
from app.models.device import Device


async def create_device(device: Device, db_name='devices.db'):
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as cursor:
            # Check if the user_id exists
            await cursor.execute("SELECT id FROM coordinates WHERE latitude = ? AND longitude = ?",
                                 (device.localisation.latitude, device.localisation.longitude))
            coordinate = await cursor.fetchone()

            if coordinate:
                coordinate_id = coordinate[0]
            else:
                # If coordinate_id doesn't exist, create a new  coordinate
                await cursor.execute("INSERT INTO coordinates (latitude, longitude) VALUES (?, ?)",
                                     (device.localisation.latitude, device.localisation.longitude))
                await db.commit()
                coordinate_id = cursor.lastrowid  # Retrieve the last inserted user_id

            # Insert the coordinate
            await cursor.execute("INSERT INTO devices (device_uuid, localisation_id, deployment_date, owner) "
                                 "VALUES (?, ?, ?, ?)",
                                 (device.device_uuid, coordinate_id, device.deployment_date, device.owner))
            await db.commit()


async def get_device(device_uuid: str, db_name='devices.db'):
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT devices.device_uuid, devices.deployment_date, devices.owner, "
                                 "coordinates.latitude, coordinates.longitude FROM devices INNER JOIN coordinates ON "
                                 "coordinates.id = devices.localisation_id WHERE device_uuid = ?",
                                 (device_uuid, ))
            device_data = await cursor.fetchone()

            if device_data:
                # Get column names from the cursor's description attribute
                column_names = [desc[0] for desc in cursor.description]

                # Create a dictionary to associate column names with values
                device_dict = dict(zip(column_names, device_data))

                return device_dict
            else:
                return None


async def update_device(device: Device, db_name='devices.db'):
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as cursor:

            # Check if the coordinates exists
            await cursor.execute("SELECT id FROM coordinates WHERE latitude = ? AND longitude = ?",
                                 (device.localisation.latitude, device.localisation.longitude))
            coordinate = await cursor.fetchone()

            if coordinate:
                coordinate_id = coordinate[0]
            else:
                # If coordinate_id doesn't exist, create a new coordinate
                await cursor.execute("INSERT INTO coordinates (latitude, longitude) VALUES (?, ?)",
                                     (device.localisation.latitude, device.localisation.longitude))
                await db.commit()
                coordinate_id = cursor.lastrowid  # Retrieve the last inserted row ID

            # Update the device with the new data
            await cursor.execute(
                "UPDATE devices "
                "SET deployment_date = ?, owner = ?, localisation_id = ? "
                "WHERE devices.device_uuid = ?",
                (device.deployment_date, device.owner, coordinate_id, device.device_uuid)
            )
            await db.commit()


async def delete_device(device_uuid: str, db_name='devices.db'):
    async with aiosqlite.connect(db_name) as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM devices "
                                 "WHERE device_uuid = ?",
                                 (device_uuid, ))
            await db.commit()
