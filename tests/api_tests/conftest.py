import pytest
from guess_number.routes import sessions

@pytest.fixture(autouse=True)
def session_clearance():
    sessions.clear()
    yield
    sessions.clear()
    