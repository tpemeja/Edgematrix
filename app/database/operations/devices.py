"""
Module containing CRUD operations for devices using an SQLite database.
"""

import aiosqlite
from app.models.device import Device


async def create_device(device: Device, db_name='devices.db'):
    """
    Creates a new device in the database.

    If the coordinates for the device's location do not exist, they are first created
    in the 'coordinates' table.
    The device information, including UUID, deployment date, and owner, is then inserted
    into the 'devices' table.

    Parameters:
    - device (Device): The device object containing information to be inserted.
    - db_name (str): The name of the SQLite database file. Default is 'devices.db'.
    """
    async with aiosqlite.connect(db_name) as database:
        async with database.cursor() as cursor:
            # Check if the coordinates exist
            await cursor.execute("SELECT id FROM coordinates WHERE latitude = ? AND longitude = ?",
                                 (device.localisation.latitude, device.localisation.longitude))
            coordinate = await cursor.fetchone()

            if coordinate:
                coordinate_id = coordinate[0]
            else:
                # If coordinate_id doesn't exist, create a new coordinate
                await cursor.execute("INSERT INTO coordinates (latitude, longitude) VALUES (?, ?)",
                                     (device.localisation.latitude, device.localisation.longitude))
                await database.commit()
                coordinate_id = cursor.lastrowid  # Retrieve the last inserted row ID

            # Insert the device
            await cursor.execute(
                "INSERT INTO devices (device_uuid, localisation_id, deployment_date, owner) "
                "VALUES (?, ?, ?, ?)",
                (device.device_uuid, coordinate_id, device.deployment_date, device.owner))
            await database.commit()


async def get_device(device_uuid: str, db_name='devices.db'):
    """
    Retrieves a device from the database based on its UUID.

    Parameters:
    - device_uuid (str): The UUID of the device to retrieve.
    - db_name (str): The name of the SQLite database file. Default is 'devices.db'.

    Returns:
    - dict or None: A dictionary containing device information if found, else None.
    """
    async with aiosqlite.connect(db_name) as database:
        async with database.cursor() as cursor:
            await cursor.execute(
                "SELECT devices.device_uuid, devices.deployment_date, devices.owner, "
                "coordinates.latitude, coordinates.longitude "
                "FROM devices INNER JOIN coordinates "
                "ON coordinates.id = devices.localisation_id "
                "WHERE device_uuid = ?",
                (device_uuid,))
            device_data = await cursor.fetchone()

            if device_data:
                # Get column names from the cursor's description attribute
                column_names = [desc[0] for desc in cursor.description]

                # Create a dictionary to associate column names with values
                device_dict = dict(zip(column_names, device_data))

                # Create a 'localisation' dictionary with latitude and longitude keys
                device_dict['localisation'] = {
                    'latitude': device_dict.pop('latitude'),
                    'longitude': device_dict.pop('longitude')
                }

                return device_dict

            return None


async def update_device(device: Device, db_name='devices.db'):
    """
    Updates an existing device in the database with new information.

    If the coordinates for the updated location do not exist, they are first created
    in the 'coordinates' table.

    Parameters:
    - device (Device): The updated device object.
    - db_name (str): The name of the SQLite database file. Default is 'devices.db'.
    """
    async with aiosqlite.connect(db_name) as database:
        async with database.cursor() as cursor:
            # Check if the coordinates exist
            await cursor.execute("SELECT id FROM coordinates WHERE latitude = ? AND longitude = ?",
                                 (device.localisation.latitude, device.localisation.longitude))
            coordinate = await cursor.fetchone()

            if coordinate:
                coordinate_id = coordinate[0]
            else:
                # If coordinate_id doesn't exist, create a new coordinate
                await cursor.execute("INSERT INTO coordinates (latitude, longitude) VALUES (?, ?)",
                                     (device.localisation.latitude, device.localisation.longitude))
                await database.commit()
                coordinate_id = cursor.lastrowid  # Retrieve the last inserted row ID

            # Update the device with the new data
            await cursor.execute(
                "UPDATE devices "
                "SET deployment_date = ?, owner = ?, localisation_id = ? "
                "WHERE devices.device_uuid = ?",
                (device.deployment_date, device.owner, coordinate_id, device.device_uuid)
            )
            await database.commit()


async def delete_device(device_uuid: str, db_name='devices.db'):
    """
    Deletes a device from the database based on its UUID.

    Parameters:
    - device_uuid (str): The UUID of the device to delete.
    - db_name (str): The name of the SQLite database file. Default is 'devices.db'.
    """
    async with aiosqlite.connect(db_name) as database:
        async with database.cursor() as cursor:
            await cursor.execute("DELETE FROM devices "
                                 "WHERE device_uuid = ?",
                                 (device_uuid,))
            await database.commit()
