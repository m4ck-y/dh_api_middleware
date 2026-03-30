import os
import pytest
from fastapi.testclient import TestClient

os.environ["SERVICE_HEALTH_MONITORING_URL"] = (
    "http://127.0.0.1:8001/api/health-monitoring"
)

from app.main import app


@pytest.fixture(scope="function")
def client():
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
