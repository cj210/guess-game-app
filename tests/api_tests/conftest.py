import pytest
from guess_number.routes import sessions, users
from api_tests.clients.gga_client import GgaClient

@pytest.fixture(autouse=True, scope="function")
def api_client():
    users.clear()
    sessions.clear()
    client = GgaClient()
    with client.http_client:
        yield client
    users.clear()
    sessions.clear()
    
    