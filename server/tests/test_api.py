import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.database import Base

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # create tables fresh for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # teardown if needed
    Base.metadata.drop_all(bind=engine)


def test_report_and_list():
    payload = {
        "machine_id": "machine-123",
        "hostname": "test-host",
        "os_name": "Ubuntu",
        "os_version": "22.04",
        "checks": [
            {"name": "disk_encryption", "status": "ok"},
            {"name": "os_update", "status": "outdated"}
        ]
    }
    r = client.post("/api/report", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["machine_id"] == "machine-123"
    assert data["hostname"] == "test-host"
    # list
    r2 = client.get("/api/machines")
    assert r2.status_code == 200
    arr = r2.json()
    assert isinstance(arr, list)
    assert len(arr) >= 1
