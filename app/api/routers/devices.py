from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.device import Device, DeviceNotFoundResponse, DeviceAlreadyExists, DeviceDeletionResponse
from app.database.operations import devices
from typing import Annotated

router = APIRouter()


@router.post(path="/",
             summary="Create a Device",
             description="Create a new device.",
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_201_CREATED: {"model": Device},
                 status.HTTP_409_CONFLICT: {"model": DeviceAlreadyExists}
             })
def create_device(device: Device):
    """
    Create a new device.

    Parameters:
    - `device`: The device details to create.
    """
    item = devices.get_device(device.device_uuid)

    if item is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=jsonable_encoder(DeviceAlreadyExists()))

    devices.create_device(device)

    return device


@router.get(path="/{device_uuid}",
            summary="Read a Device",
            description="Read a device by its UUID.",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {"model": Device},
                status.HTTP_404_NOT_FOUND: {"model": DeviceNotFoundResponse}
            })
def read_device(device_uuid: Annotated[str, Path(pattern=Device.UUID_REGEX_PATTERN,
                                                 examples=["DEVX000001"],
                                                 description="The uuid of the device. It should start with the "
                                                             "prefix (DEV), a single variable character [A-Z], "
                                                             "and six integers.")]):
    """
    Read a device by its UUID.

    Parameters:
    - `device_uuid`: The UUID of the device to read.
    """
    item = devices.get_device(device_uuid)

    if item is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(DeviceNotFoundResponse()))

    return item


@router.put(path="/",
            summary="Update a Device",
            description="Update a device by providing its updated details.",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {"model": Device},
                status.HTTP_404_NOT_FOUND: {"model": DeviceNotFoundResponse}
            })
def update_device(device: Device):
    """
    Update a device by providing its updated details.

    Parameters:
    - `device`: The updated device details, including its UUID.
    """
    item = devices.get_device(device.device_uuid)

    if item is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(DeviceNotFoundResponse()))

    devices.update_device(device)

    return device


@router.delete(path="/{device_uuid}",
               summary="Delete a Device",
               description="Delete a device by its UUID.",
               status_code=status.HTTP_200_OK,
               responses={
                   status.HTTP_200_OK: {"model": DeviceDeletionResponse},
                   status.HTTP_404_NOT_FOUND: {"model": DeviceNotFoundResponse}
               })
def delete_device(device_uuid: Annotated[str, Path(pattern=Device.UUID_REGEX_PATTERN,
                                                   examples=["DEVX000001"],
                                                   description="The uuid of the device. It should start with "
                                                               "the prefix (DEV), a single variable character ["
                                                               "A-Z], and six integers.")]):
    """
    Delete a device by its UUID.

    Parameters:
    - `device_uuid`: The UUID of the device to delete.
    """

    item = devices.get_device(device_uuid)

    if item is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(DeviceNotFoundResponse()))

    devices.delete_device(device_uuid)

    return DeviceDeletionResponse()
