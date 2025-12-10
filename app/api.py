from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from .database import get_session
from .models import Server
from fastapi import APIRouter

router = APIRouter()


# Health check endpoint
@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "pgbench-api"}


# Server management endpoints
@router.post("/servers/", response_model=Server)
def create_server(server: Server, session: Session = Depends(get_session)):
    """Create a new PostgreSQL server configuration"""
    db_server = Server.model_validate(server)
    session.add(db_server)
    session.commit()
    session.refresh(db_server)
    return db_server


@router.get("/servers/", response_model=List[Server])
def read_servers(session: Session = Depends(get_session)):
    """Get all configured PostgreSQL servers"""
    servers = session.exec(select(Server)).all()
    return servers


@router.get("/servers/{server_id}", response_model=Server)
def read_server(server_id: int, session: Session = Depends(get_session)):
    """Get a specific PostgreSQL server configuration"""
    server = session.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.put("/servers/{server_id}", response_model=Server)
def update_server(
    server_id: int, server: Server, session: Session = Depends(get_session)
):
    """Update a PostgreSQL server configuration"""
    db_server = session.get(Server, server_id)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    server_data = server.model_dump(exclude_unset=True)
    for key, value in server_data.items():
        setattr(db_server, key, value)

    session.add(db_server)
    session.commit()
    session.refresh(db_server)
    return db_server


@router.delete("/servers/{server_id}")
def delete_server(server_id: int, session: Session = Depends(get_session)):
    """Delete a PostgreSQL server configuration"""
    server = session.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    session.delete(server)
    session.commit()
    return {"message": "Server deleted successfully"}
