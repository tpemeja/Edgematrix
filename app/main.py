from fastapi import FastAPI
from app.database.startup import setup_database
from app.api.routers import devices

app = FastAPI()


@app.on_event("startup")
async def startup():
    await setup_database()

# Include the API routers
app.include_router(devices.router, prefix="/devices", tags=["devices"])
