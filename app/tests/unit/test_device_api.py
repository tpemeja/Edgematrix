from fastapi.testclient import TestClient
from app.models.device import Device, DeviceDeletionResponse

from app.main import app

DEVICE_DATA = Device.model_config["json_schema_extra"]["example"]


def test_create_device():
    # Test creating a new device
    with TestClient(app) as client:
        response = client.post("/devices/", json=DEVICE_DATA)

    assert response.status_code == 201  # Check status code
    assert response.json() == DEVICE_DATA  # Check response data


def test_read_device():
    # Test reading an existing device
    with TestClient(app) as client:
        response = client.get(f"/devices/{DEVICE_DATA['device_uuid']}")

    assert response.status_code == 200  # Check status code
    assert response.json() == DEVICE_DATA  # Check response data


def test_update_device():
    # Test updating an existing device
    updated_device_data = {
        "device_uuid": "DEVX000001",
        "localisation": {"latitude": 35.6582, "longitude": 139.8752},
        "deployment_date": "2024-03-14",
        "owner": "updated_owner@example.com"
    }
    with TestClient(app) as client:
        response = client.put("/devices/", json=updated_device_data)

    assert response.status_code == 200  # Check status code
    assert response.json() == updated_device_data  # Check response data


def test_delete_device():
    # Test deleting an existing device
    with TestClient(app) as client:
        response = client.delete(f"/devices/{DEVICE_DATA['device_uuid']}")

    assert response.status_code == 200  # Check status code
    assert response.json() == vars(DeviceDeletionResponse())  # Check response data
