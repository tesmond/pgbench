from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import router as api_router
from .database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield


app = FastAPI(
    title="PGBench API",
    description="REST API for PostgreSQL",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(api_router)
