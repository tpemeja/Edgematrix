import sqlite3
from app.models.device import Device


def create_device(device: Device, db_name='devices.db'):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        # Check if the coordinates exist
        cursor.execute("SELECT id FROM coordinates WHERE latitude = ? AND longitude = ?",
                       (device.localisation.latitude, device.localisation.longitude))
        coordinate = cursor.fetchone()

        if coordinate:
            coordinate_id = coordinate[0]
        else:
            # If coordinate_id doesn't exist, create a new coordinate
            cursor.execute("INSERT INTO coordinates (latitude, longitude) VALUES (?, ?)",
                           (device.localisation.latitude, device.localisation.longitude))
            db.commit()
            coordinate_id = cursor.lastrowid  # Retrieve the last inserted row ID

        # Insert the device
        cursor.execute("INSERT INTO devices (device_uuid, localisation_id, deployment_date, owner) "
                       "VALUES (?, ?, ?, ?)",
                       (device.device_uuid, coordinate_id, device.deployment_date, device.owner))
        db.commit()


def get_device(device_uuid: str, db_name='devices.db'):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        cursor.execute("SELECT devices.device_uuid, devices.deployment_date, devices.owner, "
                       "coordinates.latitude, coordinates.longitude FROM devices INNER JOIN coordinates ON "
                       "coordinates.id = devices.localisation_id WHERE device_uuid = ?",
                       (device_uuid,))
        device_data = cursor.fetchone()

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
        else:
            return None


def update_device(device: Device, db_name='devices.db'):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        # Check if the coordinates exist
        cursor.execute("SELECT id FROM coordinates WHERE latitude = ? AND longitude = ?",
                       (device.localisation.latitude, device.localisation.longitude))
        coordinate = cursor.fetchone()

        if coordinate:
            coordinate_id = coordinate[0]
        else:
            # If coordinate_id doesn't exist, create a new coordinate
            cursor.execute("INSERT INTO coordinates (latitude, longitude) VALUES (?, ?)",
                           (device.localisation.latitude, device.localisation.longitude))
            db.commit()
            coordinate_id = cursor.lastrowid  # Retrieve the last inserted row ID

        # Update the device with the new data
        cursor.execute(
            "UPDATE devices "
            "SET deployment_date = ?, owner = ?, localisation_id = ? "
            "WHERE devices.device_uuid = ?",
            (device.deployment_date, device.owner, coordinate_id, device.device_uuid)
        )
        db.commit()


def delete_device(device_uuid: str, db_name='devices.db'):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        cursor.execute("DELETE FROM devices "
                       "WHERE device_uuid = ?",
                       (device_uuid,))
        db.commit()
