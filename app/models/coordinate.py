"""
Module containing the Coordinate model definition.
"""

from pydantic import BaseModel, Field, field_validator


class Coordinate(BaseModel):
    """
    Represents a geographical coordinate with latitude and longitude.

    Attributes:
    - latitude (float): The latitude in decimal degrees, must be between -90 and 90.
    - longitude (float): The longitude in decimal degrees, must be between -180 and 180.
    """
    latitude: float = Field(default=...,
                            description="Latitude in decimal degrees. "
                                        "Must be between -90 and 90.")
    longitude: float = Field(default=...,
                             description="Longitude in decimal degrees. "
                                         "Must be between -180 and 180.")

    @classmethod
    @field_validator('latitude')
    def validate_latitude(cls, value):
        """
        Validates the latitude value to ensure it falls within the range of -90 to 90 degrees.

        Parameters:
        - value (float): The latitude value to validate.

        Returns:
        - float: The validated latitude value.

        Raises:
        - ValueError: If the latitude value is outside the valid range.
        """
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return value

    @classmethod
    @field_validator('longitude')
    def validate_longitude(cls, value):
        """
        Validates the longitude value to ensure it falls within the range of -180 to 180 degrees.

        Parameters:
        - value (float): The longitude value to validate.

        Returns:
        - float: The validated longitude value.

        Raises:
        - ValueError: If the longitude value is outside the valid range.
        """
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "latitude": 35.6582,
                "longitude": 139.8752
            }
        }
    }
