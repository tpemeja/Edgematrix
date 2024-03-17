from fastapi import FastAPI
from app.database.startup import setup_database
from app.api.routers import devices

setup_database()

app = FastAPI()

# Include the API routers
app.include_router(devices.router, prefix="/devices", tags=["devices"])
