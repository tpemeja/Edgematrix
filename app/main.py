from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.startup import setup_database
from app.api.routers import devices


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        # Perform any setup tasks here
        setup_database()
        yield
    finally:
        # Clean up tasks can be performed here if needed
        pass

app = FastAPI(lifespan=lifespan)

# Include the API routers
app.include_router(devices.router, prefix="/devices", tags=["devices"])
