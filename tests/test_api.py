import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app
from app.models import Server


@pytest.fixture(name="session")
def session_fixture():
    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Override the get_session dependency to use the test session
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "pgbench-api"}


def test_create_server(client: TestClient, session: Session):
    server_data = {
        "host": "localhost",
        "port": 5432,
        "name": "test_server",
        "database": "test_db",
        "username": "test_user",
        "description": "Test server",
    }
    response = client.post("/servers/", json=server_data)
    assert response.status_code == 200
    data = response.json()
    assert data["host"] == "localhost"
    assert data["name"] == "test_server"
    assert "id" in data


def test_read_servers_empty(client: TestClient):
    response = client.get("/servers/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_servers_with_data(client: TestClient, session: Session):
    # Create a server first
    server = Server(host="localhost", name="test_server")
    session.add(server)
    session.commit()

    response = client.get("/servers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "test_server"


def test_read_server(client: TestClient, session: Session):
    # Create a server first
    server = Server(host="localhost", name="test_server")
    session.add(server)
    session.commit()

    response = client.get(f"/servers/{server.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_server"


def test_read_server_not_found(client: TestClient):
    response = client.get("/servers/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Server not found"}


def test_update_server(client: TestClient, session: Session):
    # Create a server first
    server = Server(host="localhost", name="test_server")
    session.add(server)
    session.commit()

    update_data = {
        "host": "localhost",
        "name": "updated_server",
        "description": "Updated description",
    }
    response = client.put(f"/servers/{server.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated_server"
    assert data["description"] == "Updated description"


def test_update_server_not_found(client: TestClient):
    update_data = {"host": "localhost", "name": "test"}
    response = client.put("/servers/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Server not found"}


def test_delete_server(client: TestClient, session: Session):
    # Create a server first
    server = Server(host="localhost", name="test_server")
    session.add(server)
    session.commit()

    response = client.delete(f"/servers/{server.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Server deleted successfully"}

    # Verify it's deleted
    response = client.get(f"/servers/{server.id}")
    assert response.status_code == 404


def test_delete_server_not_found(client: TestClient):
    response = client.delete("/servers/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Server not found"}
