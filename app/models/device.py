from pydantic import BaseModel, field_validator, Field, EmailStr
from typing import ClassVar
import re
from datetime import date
from app.models.coordinate import Coordinate


class Device(BaseModel):
    UUID_REGEX_PATTERN: ClassVar[str] = r'^DEV[A-Z]\d{6}$'

    device_uuid: str = Field(default=...,
                             description="The uuid of the device. It should start with the prefix (DEV), "
                                         "a single variable character [A-Z], and six integers (e.g., DEVX000001)")

    localisation: Coordinate = Field(default=None,
                                     description="The user's location as latitude and longitude coordinates")

    deployment_date: date = Field(default=None,
                                  description="The deployment date in the format YYYY-MM-DD")
    owner: EmailStr = Field(default=...,
                            description="The user's location as latitude and longitude coordinates")

    @classmethod
    @field_validator('device_uuid')
    def name_must_be_uuid_format(cls, uuid: str) -> str:
        if not re.match(pattern=cls.UUID_REGEX_PATTERN, string=uuid):
            raise ValueError("Invalid name format. It must start with 'DEV', "
                             "followed by a single uppercase letter and six digits (e.g., DEVX000001).")
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
    message: str = "Device not found"


class DeviceAlreadyExists(BaseModel):
    message: str = "Device already exists"


class DeviceDeletionResponse(BaseModel):
    message: str = "Device successfully deleted"
