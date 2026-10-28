import pytest
from fastapi.testclient import TestClient
from guess_number.app import forest
from httpx2 import Response


class TestRegister:
    
    def test_user_register_with_valid_inputs(self):
        client: TestClient = TestClient(forest)
        payload: dict = {
            "username": "kacha",
            "password": "asd"
        }
        response: Response = client.post("/register", json=payload)
        assert response.status_code == 201
        assert response.json().get("detail") == "User creation successfull!"
        assert response.json().get("message") == "New user kacha created!"
    
    def test_user_register_with_existing_username(self):
        client: TestClient = TestClient(forest)
        payload: dict = {
            "username": "kacha",
            "password": "asd"
        }
        client.post("/register", json=payload)
        response: Response = client.post("/register", json=payload)
        assert response.status_code == 409
        assert response.json().get("detail") == "User already exist!"
    



'''
class TestSessions:
    
    def test_session_creation(self):
        test_client: TestClient = TestClient(bisket)
        response: Response = test_client.post("/sessions")
        assert response.status_code == 200
        assert response.json().get("session_id", None)
        assert response.json().get("status", None) == "running"
    
    def test_unique_session_ids(self):
        test_client: TestClient = TestClient(bisket)
        response1: Response = test_client.post("/sessions")
        response2: Response = test_client.post("/sessions")
        assert response1.json()["session_id"] != response2.json()["session_id"]
    
class TestGuesses:

    @pytest.mark.parametrize(
        "inp",
        [
            "2", "50", "1", "100"
        ]
    )
    def test_valid_guess(self, inp):
        test_client: TestClient = TestClient(bisket)
        session_id: str = test_client.post("/sessions").json()["session_id"]
        response: Response= test_client.post(f"/sessions/{session_id}/guesses", json={"guess": inp})
        assert response.status_code == 200
        assert response.json()["attempts"] == 4
    
    def test_invalid_session(self):
        test_client: TestClient = TestClient(bisket)
        session_id: str = test_client.post("/sessions").json()["session_id"]
        response: Response = test_client.post(f"/sessions/{session_id}xx/guesses", json={"guess": "54"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Session doesn't exist"

    @pytest.mark.parametrize(
        "inp",
        [
            "abc", "0", "-1", "101"
        ]
    )
    def test_invalid_input(self, inp):
        test_client: TestClient = TestClient(bisket)
        session_id: str = test_client.post("/sessions").json()["session_id"]
        invalid_response: Response = test_client.post(f"/sessions/{session_id}/guesses", json={"guess": inp})
        assert invalid_response.status_code == 422
        assert invalid_response.json()["detail"] == "Unprocessible entity: Please enter number between 1 and 100"
        valid_response: Response = test_client.post(f"/sessions/{session_id}/guesses", json={"guess": "55"})
        assert valid_response.json()["attempts"] == 4
    
    @pytest.mark.parametrize(
        "inp, exp, st",
        [
            ("55", "Too Low", "running"),
            ("95", "Too High", "running"),
            ("75", "You got it", "complete")
        ]
    )
    def test_message_and_status_for_valid_input(self,mocker, inp, exp, st):
        mocker.patch("guess_number.core.randint", return_value=75)
        test_client: TestClient = TestClient(bisket)
        session_id: str = test_client.post("/sessions").json()["session_id"]
        response: Response = test_client.post(f"/sessions/{session_id}/guesses", json={"guess": inp})
        assert response.status_code == 200
        assert response.json()["attempts"] == 4
        assert response.json()["status"] == st
        assert response.json()["message"] == exp

    def test_sessions_have_independent_attempts(self, mocker):
        mocker.patch("guess_number.core.randint", return_value=75)
        test_client: TestClient = TestClient(bisket)
        session_id1: str = test_client.post("/sessions").json()["session_id"]
        session_id2: str = test_client.post("/sessions").json()["session_id"]
        assert session_id1 != session_id2
        response1_first: Response = test_client.post(f"/sessions/{session_id1}/guesses", json={"guess": "55"})
        assert response1_first.json()["attempts"] == 4
        response2_first: Response = test_client.post(f"/sessions/{session_id2}/guesses", json={"guess": "85"})
        assert response2_first.json()["attempts"] == 4
        response2_second: Response = test_client.post(f"/sessions/{session_id2}/guesses", json={"guess": "65"})
        assert response2_second.json()["attempts"] == 3
        response1_second: Response = test_client.post(f"/sessions/{session_id1}/guesses", json={"guess": "65"})
        assert response1_second.json()["attempts"] == 3
    
    def test_session_complete(self, mocker):
        mocker.patch("guess_number.core.randint", return_value=75)
        test_client: TestClient = TestClient(bisket)
        session_id: str = test_client.post("/sessions").json()["session_id"]
        for iter in range(4,-1,-1):
            response: Response = test_client.post(f"/sessions/{session_id}/guesses", json={"guess": "55"})
            assert response.status_code == 200
            assert response.json()["attempts"] == iter
            if iter:
                assert response.json()["status"] == "running"
            else:
                assert response.json()["status"] == "complete"
        response: Response = test_client.post(f"/sessions/{session_id}/guesses", json={"guess": "55"})
        assert response.status_code == 409
        assert response.json()["detail"] == "Not available for a completed session"
                
        
'''