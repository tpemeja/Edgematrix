"""
Module containing unit tests for device-related endpoints.
"""

from fastapi.testclient import TestClient
from fastapi import status
from app.models.device import DeviceDeletionResponse, DeviceAlreadyExists, DeviceNotFoundResponse

from app.main import app

DEVICE_DATA = {
    "device_uuid": "DEVX000001",
    "localisation":
        {
            "latitude": 35.6582,
            "longitude": 139.8752
        },
    "deployment_date": "2024-03-14",
    "owner": "owner@example.com"
}

UPDATED_DEVICE_DATA = {
    "device_uuid": "DEVX000001",
    "localisation":
        {
            "latitude": 35.6582,
            "longitude": 139.8752
        },
    "deployment_date": "2024-03-14",
    "owner": "updated_owner@example.com"
}

NON_EXISTING_DEVICE_DATA = {
    "device_uuid": "DEVX000002",
    "owner": "owner@example.com"
}


def test_create_device():
    """
    Test creating a new device.
    """
    with TestClient(app) as client:
        response = client.post("/devices/", json=DEVICE_DATA)

    assert response.status_code == status.HTTP_201_CREATED  # Check status code
    assert response.json() == DEVICE_DATA  # Check response data


def test_create_duplicate_device():
    """
    Test creating a device already existing.
    """
    with TestClient(app) as client:
        response = client.post("/devices/", json=DEVICE_DATA)

    assert response.status_code == status.HTTP_409_CONFLICT  # Check status code
    assert response.json() == vars(DeviceAlreadyExists())  # Check response data


def test_read_device():
    """
    Test reading an existing device.
    """
    with TestClient(app) as client:
        response = client.get(f"/devices/{DEVICE_DATA['device_uuid']}")

    assert response.status_code == status.HTTP_200_OK  # Check status code
    assert response.json() == DEVICE_DATA  # Check response data


def test_read_non_existing_device():
    """
    Test reading a non-existing device.
    """
    with TestClient(app) as client:
        response = client.get(f"/devices/{NON_EXISTING_DEVICE_DATA['device_uuid']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND  # Check status code
    assert response.json() == vars(DeviceNotFoundResponse())  # Check response data


def test_update_device():
    """
    Test updating an existing device.
    """
    with TestClient(app) as client:
        response = client.put("/devices/", json=UPDATED_DEVICE_DATA)

    assert response.status_code == status.HTTP_200_OK  # Check status code
    assert response.json() == UPDATED_DEVICE_DATA  # Check response data


def test_delete_device():
    """
    Test deleting an existing device.
    """
    with TestClient(app) as client:
        response = client.delete(f"/devices/{DEVICE_DATA['device_uuid']}")

    assert response.status_code == status.HTTP_200_OK  # Check status code
    assert response.json() == vars(DeviceDeletionResponse())  # Check response data


def test_delete_deleted_device():
    """
    Test deleting a deleted device.
    """
    with TestClient(app) as client:
        response = client.delete(f"/devices/{DEVICE_DATA['device_uuid']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND  # Check status code
    assert response.json() == vars(DeviceNotFoundResponse())  # Check response data
