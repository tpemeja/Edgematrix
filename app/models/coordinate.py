from pydantic import BaseModel, Field, field_validator


class Coordinate(BaseModel):
    latitude: float = Field(..., description="Latitude in decimal degrees")
    longitude: float = Field(..., description="Longitude in decimal degrees")

    @classmethod
    @field_validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return v

    @classmethod
    @field_validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "latitude": 35.6582,
                "longitude": 139.8752
            }
        }
    }
