import os

from sqlmodel import Session, SQLModel, create_engine

# Default to SQLite for local development, but support PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Create engine with appropriate settings
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(
        DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
    )


def create_db_and_tables():
    """Create database tables based on SQLModel definitions"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def get_postgres_connection_string(
    host: str, port: int, database: str, username: str, password: str
) -> str:
    """Helper function to create PostgreSQL connection string for pgbench"""
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"
