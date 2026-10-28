import pytest
from guess_number.routes import sessions, users

@pytest.fixture(autouse=True)
def session_clearance():
    users.clear()
    sessions.clear()
    yield
    users.clear()
    sessions.clear()
    