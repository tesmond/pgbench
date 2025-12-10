from fastapi import FastAPI
from .api import router as api_router
from .routers.pgbench import router as pgbench_router
from .database import create_db_and_tables

app = FastAPI(
    title="PGBench API", description="REST API for PostgreSQL", version="0.1.0"
)

# Include routers
app.include_router(api_router)
app.include_router(pgbench_router, prefix="/pgbench")


# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
