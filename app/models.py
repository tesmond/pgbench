from sqlmodel import SQLModel, Field
from typing import Optional


class Server(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    host: str
    port: int = Field(default=5432)
    name: str
    database: str = Field(default="postgres")
    username: Optional[str] = None
    description: Optional[str] = None
