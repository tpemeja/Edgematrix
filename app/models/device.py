"""
Module containing the Device model definition.
"""

from typing import ClassVar
from datetime import date
import re
from pydantic import BaseModel, Field, field_validator, EmailStr
from app.models.coordinate import Coordinate


class Device(BaseModel):
    """
    Represents a device with unique identifiers and location information.

    Attributes:
    - device_uuid (str): The UUID of the device. It should start with the prefix (DEV),
      followed by a single uppercase letter and six digits (e.g., DEVX000001).
    - localisation (Coordinate): Geographical location of the device as coordinates.
    - deployment_date (date): The deployment date of the device in the format YYYY-MM-DD.
    - owner (EmailStr): The email address of the owner of the device.
    """
    UUID_REGEX_PATTERN: ClassVar[str] = r'^DEV[A-Z]\d{6}$'

    device_uuid: str = Field(default=...,
                             description="The UUID of the device. "
                                         "It should start with the prefix (DEV), "
                                         "a single uppercase letter, "
                                         "and six digits (e.g., DEVX000001)")

    localisation: Coordinate = Field(default=None,
                                     description="The geographical location of the device "
                                                 "as latitude and longitude coordinates")

    deployment_date: date = Field(default=None,
                                  description="The deployment date of the device "
                                              "in the format YYYY-MM-DD")
    owner: EmailStr = Field(default=...,
                            description="The email address of the owner of the device")

    @classmethod
    @field_validator('device_uuid')
    def name_must_be_uuid_format(cls, uuid: str) -> str:
        """
        Validates the format of the device UUID.

        Parameters:
        - uuid (str): The device UUID to validate.

        Returns:
        - str: The validated device UUID.

        Raises:
        - ValueError: If the device UUID format is invalid.
        """
        if not re.match(pattern=cls.UUID_REGEX_PATTERN, string=uuid):
            raise ValueError("Invalid name format. "
                             "It must start with 'DEV', followed by a single uppercase letter "
                             "and six digits (e.g., DEVX000001).")
        return uuid

    model_config = {
        "json_schema_extra": {
            "example": {
                "device_uuid": "DEVX000001",
                "localisation": {
                    "latitude": 35.6582,
                    "longitude": 139.8752
                },
                "deployment_date": "2024-03-14",
                "owner": "tpemeja@edgematrix.com"
            }
        }
    }


class DeviceNotFoundResponse(BaseModel):
    """
    Represents a response indicating that the device was not found.
    """
    message: str = "Device not found"


class DeviceAlreadyExists(BaseModel):
    """
    Represents a response indicating that the device already exists.
    """
    message: str = "Device already exists"


class DeviceDeletionResponse(BaseModel):
    """
    Represents a response indicating that the device was successfully deleted.
    """
    message: str = "Device successfully deleted"
