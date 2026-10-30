import pytest
from guess_number.models import SessionObject




class TestRegister:
    
    @pytest.mark.parametrize(
        "username, password",
        [
            ("kacha", "asd"),
            ("12345", "094504"),
            (")(&&)", "$%^")
        ]
    )
    def test_user_register_with_valid_inputs(self, api_client, username, password):
        response = api_client.user_register(username, password)
        assert response.status_code == 201
        assert response.json().get("detail") == "User creation successfull!"
        assert response.json().get("message") == f"New user {username} created!"
    
    @pytest.mark.parametrize(
        "username, password",
        [
            ("kacha", "asd"),
            ("12345", "094504"),
            (")(&&)", "$%^")
        ]
    )
    def test_user_register_with_existing_username(self, api_client, username, password):
        response1 = api_client.user_register(username, password)
        response2 = api_client.user_register(username, password)
        assert response1.status_code == 201
        assert response1.json().get("detail") == "User creation successfull!"
        assert response1.json().get("message") == f"New user {username} created!"
        assert response2.status_code == 409
        assert response2.json().get("detail") == "User already exist!"
    
    
class TestUserLogin:
    
    @pytest.mark.parametrize(
        "username, password",
        [
            ("kacha", "asd"),
            ("12345", "094504"),
            (")(&&)", "$%^")
        ]
    )
    def test_user_login_with_valid_data(self, api_client, username, password):
        reg_response = api_client.user_register(username, password)
        log_response = api_client.user_login(username, password)
        assert reg_response.status_code == 201
        assert log_response.status_code == 200
        assert log_response.json().get("detail") == "User Login successfull!"
        assert log_response.json().get("message") == f"Logged in as {username}!"
        assert log_response.json().get("access_token") == api_client.token
    
    @pytest.mark.parametrize(
        "username, password",
        [
            ("Right user", "Wrong password"),
            ("Wrong user", "Right password"),
            ("12345", "ding"),
            (")(&&)", "$%^")
        ]
    )
    def test_user_login_with_invalid_user_data(self, api_client, username, password):
        reg_response = api_client.user_register("Right user", "Right password")
        log_response = api_client.user_login(username, password)
        assert reg_response.status_code == 201
        assert log_response.status_code == 401
        assert log_response.json()["detail"] == "Invalid username or password!"

class TestCreateSessions:

    @pytest.mark.parametrize(
        "username, password",
        [
            ("kacha", "asd"),
            ("12345", "094504"),
            (")(&&)", "$%^")
        ]
    )
    def test_create_session_for_new_session(self, api_client, username, password):
        reg_response = api_client.user_register(username, password)
        log_response = api_client.user_login(username, password)
        ses_response = api_client.http_client.post("sessions", headers={"Authorization": f"Bearer {api_client.token}"})
        assert reg_response.status_code == 201
        assert log_response.status_code == 200
        assert ses_response.status_code == 201 
        assert ses_response.json().get("detail") == "Session created successfully!"
        assert "session id" in ses_response.json().get("message")


    @pytest.mark.parametrize(
        "username, password",
        [
            ("kacha", "asd"),
            ("12345", "094504"),
            (")(&&)", "$%^")
        ]
    )
    def test_create_session_for_existing_session(self, api_client, username, password):
        reg_response = api_client.user_register(username, password)
        log_response = api_client.user_login(username, password)
        ses_response1 = api_client.http_client.post("/sessions", headers={"Authorization": f"Bearer {api_client.token}"})
        sessionid1 = [x for x in ses_response1.json().get("message").split() if "-" in x][0]
        ses_response2 = api_client.http_client.post("/sessions", headers={"Authorization": f"Bearer {api_client.token}"})
        sessionid2 = [x for x in ses_response2.json().get("message").split() if "-" in x][0]
        assert reg_response.status_code == 201
        assert log_response.status_code == 200
        assert ses_response1.status_code == 201 
        assert ses_response1.json().get("detail") == "Session created successfully!"
        assert "session id" in ses_response1.json().get("message")
        assert ses_response2.status_code == 200 
        assert ses_response2.json().get("detail") == "Session already exists!"
        assert "session id" in ses_response2.json().get("message")
        assert sessionid1 == sessionid2
    
    def test_create_session_with_invalid_token(self, api_client):
        username = "kacha"
        password = "asd"
        reg_response = api_client.user_register(username, password)
        log_response = api_client.user_login(username, password)
        ses_response = api_client.http_client.post("/sessions", headers={"Authorization": f"Bearer {api_client.token+'ding'}"})
        assert reg_response.status_code == 201
        assert log_response.status_code == 200
        assert ses_response.status_code == 401
        assert ses_response.json().get("detail") == "Couldn't validate credentials"

    def test_create_session_with_missing_token(self, api_client):
        username = "kacha"
        password = "asd"
        reg_response = api_client.user_register(username, password)
        log_response = api_client.user_login(username, password)
        ses_response = api_client.http_client.post("/sessions")
        assert reg_response.status_code == 201
        assert log_response.status_code == 200
        assert ses_response.status_code == 401
        assert ses_response.json().get("detail") == "Not authenticated"

class TestRespondToGuess:
    
    @pytest.mark.parametrize(
        "secret, guess, message, status",
        [
            (55, "1", "Too Low", "running"),
            (55, "54", "Too Low", "running"),
            (55, "56", "Too High", "running"),
            (55, "100", "Too High", "running"),
            (55, "55", "You got it", "complete"),
            (2, "1", "Too Low", "running"),
            (2, "3", "Too High", "running"),
            (2, "100", "Too High", "running"),
            (2, "2", "You got it", "complete"),
            (99, "100", "Too High", "running"),
            (99, "1", "Too Low", "running"),
            (99, "98", "Too Low", "running"),
            (99, "99", "You got it", "complete"),
        ]
    )
    def test_respond_to_guess_valid_guesses(self, api_client, mocker, secret, guess, message, status):
        username = "kacha"
        password = "asd"
        secret_field = SessionObject.model_fields["secret"]
        original_factory = secret_field.default_factory
        mocker.patch.object(secret_field, "default_factory", lambda: secret)
        SessionObject.model_rebuild(force=True)
        try:
            reg_response = api_client.user_register(username, password)
            log_response = api_client.user_login(username, password)
            ses_response = api_client.http_client.post("/sessions", headers={"Authorization": f"Bearer {api_client.token}"})
            sessionid = [x for x in ses_response.json().get("message").split() if "-" in x][0]
            user_guess = {"guess": guess}
            guess_response = api_client.http_client.post(
                f"/sessions/{sessionid}/guesses",
                json=user_guess,
                headers={"Authorization": f"Bearer {api_client.token}"}
                )
            assert reg_response.status_code == 201
            assert log_response.status_code == 200
            assert ses_response.status_code == 201
            assert guess_response.status_code == 200
            assert guess_response.json().get('detail') =='Its a valid guess'
            assert guess_response.json().get('message') == message
            assert guess_response.json().get('session_status') == status
            assert guess_response.json().get("remaining_attempts") == 9
        finally:
            secret_field.default_factory = original_factory
            SessionObject.model_rebuild(force=True)
    
    @pytest.mark.parametrize(
        "guess", ["0", "101", "abc", "$%^&"]
    )
    def test_respond_to_guess_invalid_input(self, api_client, guess):
        user_guess = {"guess": guess}
        username = "kacha"
        password = "asd"
        reg_response = api_client.user_register(username, password)
        log_response = api_client.user_login(username, password)
        ses_response = api_client.http_client.post("/sessions", headers={"Authorization": f"Bearer {api_client.token}"})
        sessionid = [x for x in ses_response.json().get("message").split() if '-' in x][0]
        guess_response = api_client.http_client.post(
            f"/sessions/{sessionid}/guesses", 
            json=user_guess, 
            headers={"Authorization": f"Bearer {api_client.token}"},
            )
        assert reg_response.status_code == 201
        assert log_response.status_code == 200
        assert ses_response.status_code == 201
        assert guess_response.status_code == 422
        assert guess_response.json().get("detail") == "Unprocessable data. Please enter number between 1 and 100!"
    
    @pytest.mark.parametrize(
        "guess", ["0", "101", "abc", "$%^&"]
    )
    def test_respond_to_guess_no_attempt_consumed_for_invalid_guess(self, api_client, guess):
        user_guess1 = {"guess": guess}
        user_guess2 = {"guess": "55"}
        username = "kacha"
        password = "asd"
        reg_resp = api_client.user_register(username, password)
        log_resp = api_client.user_login(username, password)
        ses_resp = api_client.create_session()
        guess_resp1 = api_client.http_client.post(
            f"sessions/{api_client.sessionid}/guesses",
            json=user_guess1,
            headers={"Authorization": f"Bearer {api_client.token}"},
        )
        guess_resp2 = api_client.http_client.post(
            f"sessions/{api_client.sessionid}/guesses",
            json=user_guess2,
            headers={"Authorization": f"Bearer {api_client.token}"},
        )

        assert reg_resp.status_code == 201
        assert log_resp.status_code == 200
        assert ses_resp.status_code == 201
        assert guess_resp1.status_code == 422
        assert guess_resp1.json().get("detail") == ("Unprocessable data. Please enter number between 1 and 100!")
        assert guess_resp2.status_code == 200
        assert guess_resp2.json().get('remaining_attempts') == 9
        
    @pytest.mark.parametrize(
        "secret", [1, 50, 100]
    )
    def test_respond_to_guess_all_failed_attempts(self, api_client, mocker, secret):
        username = "kacha"
        password = "asd"
        secret_field = SessionObject.model_fields["secret"]
        original_factory = secret_field.default_factory
        mocker.patch.object(secret_field, "default_factory", lambda: secret)
        SessionObject.model_rebuild(force=True)
        user_guess = {"guess": "54"}
        try:
            reg_resp = api_client.user_register(username, password)
            log_resp = api_client.user_login(username, password)
            ses_resp = api_client.create_session()
            assert reg_resp.status_code == 201
            assert log_resp.status_code == 200
            assert ses_resp.status_code == 201
            for i in range(9, -1, -1):
                guess_resp = api_client.http_client.post(
                    f"sessions/{api_client.sessionid}/guesses",
                    json=user_guess,
                    headers={"Authorization": f"Bearer {api_client.token}"},
                )
                assert guess_resp.status_code == 200
                assert guess_resp.json().get("remaining_attempts") == i
                status = "complete" if i == 0 else "running"
                assert guess_resp.json().get("session_status") == status
        finally:
            secret_field.default_factory = original_factory
            SessionObject.model_rebuild(force=True)
            
    @pytest.mark.parametrize(
        "secret", [1, 50, 100]
    )
    def test_respond_to_guess_attempt_after_all_failed_attempts(self, api_client, mocker, secret):
        username = "kacha"
        password = "asd"
        secret_field = SessionObject.model_fields["secret"]
        original_factory = secret_field.default_factory
        mocker.patch.object(secret_field, "default_factory", lambda: secret)
        SessionObject.model_rebuild(force=True)
        user_guess = {"guess": "54"}
        try:
            reg_resp = api_client.user_register(username, password)
            log_resp = api_client.user_login(username, password)
            ses_resp = api_client.create_session()
            assert reg_resp.status_code == 201
            assert log_resp.status_code == 200
            assert ses_resp.status_code == 201
            for i in range(9, -1, -1):
                guess_resp = api_client.http_client.post(
                    f"sessions/{api_client.sessionid}/guesses",
                    json=user_guess,
                    headers={"Authorization": f"Bearer {api_client.token}"},
                )
                assert guess_resp.status_code == 200
                assert guess_resp.json().get("remaining_attempts") == i
                status = "complete" if i == 0 else "running"
                assert guess_resp.json().get("session_status") == status
            last_resp = api_client.http_client.post(
                f"sessions/{api_client.sessionid}/guesses",
                json=user_guess,
                headers={"Authorization": f"Bearer {api_client.token}"},
            )
            assert last_resp.status_code == 409
            assert last_resp.json().get("detail") == "No active session running for current user. Please restart game"
        finally:
            secret_field.default_factory = original_factory
            SessionObject.model_rebuild(force=True)
            
    @pytest.mark.parametrize(
        "secret", [1, 50, 100]
    )
    def test_respond_to_guess_attempt_after_successful_guess(self, api_client, mocker, secret):
        username = "kacha"
        password = "asd"
        secret_field = SessionObject.model_fields["secret"]
        original_factory = secret_field.default_factory
        mocker.patch.object(secret_field, "default_factory", lambda: secret)
        SessionObject.model_rebuild(force=True)
        user_guess = {"guess": str(secret)}
        try:
            reg_resp = api_client.user_register(username, password)
            log_resp = api_client.user_login(username, password)
            ses_resp = api_client.create_session()
            assert reg_resp.status_code == 201
            assert log_resp.status_code == 200
            assert ses_resp.status_code == 201
            right_response = api_client.http_client.post(
                f"sessions/{api_client.sessionid}/guesses",
                json=user_guess,
                headers={"Authorization": f"Bearer {api_client.token}"},
            )
            last_resp = api_client.http_client.post(
                f"sessions/{api_client.sessionid}/guesses",
                json=user_guess,
                headers={"Authorization": f"Bearer {api_client.token}"},
            )
            assert right_response.status_code == 200
            assert right_response.json().get("message") == "You got it"
            assert right_response.json().get("session_status") == "complete"
            assert last_resp.status_code == 409
            assert last_resp.json().get("detail") == "No active session running for current user. Please restart game"
        finally:
            secret_field.default_factory = original_factory
            SessionObject.model_rebuild(force=True)
            
class TestRestartSession:
    
    @pytest.mark.parametrize(
        "secret", [1, 50, 100]
    )
    def test_restart_session_restart_completed_session(self, api_client, mocker, secret):
        username = "kacha"
        password = "asd"
        secret_field = SessionObject.model_fields["secret"]
        original_factory = secret_field.default_factory
        mocker.patch.object(secret_field, "default_factory", lambda: secret)
        SessionObject.model_rebuild(force=True)
        user_guess = {"guess": str(secret)}
        try:
            reg_resp = api_client.user_register(username, password)
            log_resp = api_client.user_login(username, password)
            ses_resp = api_client.create_session()
            assert reg_resp.status_code == 201
            assert log_resp.status_code == 200
            assert ses_resp.status_code == 201
            right_resp = api_client.http_client.post(
                f"sessions/{api_client.sessionid}/guesses",
                json=user_guess,
                headers={"Authorization": f"Bearer {api_client.token}"},
            )
            res_resp = api_client.http_client.post("/sessions/restart", headers={"Authorization": f"Bearer {api_client.token}"})
            next_resp = api_client.http_client.post(
                f"sessions/{api_client.sessionid}/guesses",
                json=user_guess,
                headers={"Authorization": f"Bearer {api_client.token}"},
            )
            assert right_resp.status_code == 200
            assert right_resp.json().get("message") == "You got it"
            assert right_resp.json().get("session_status") == "complete"
            assert right_resp.json().get("remaining_attempts") == 9
            assert res_resp.status_code == 200
            assert res_resp.json().get("detail") == "Session restarted successfully!"
            assert res_resp.json().get("message") == f"Session: {api_client.sessionid} has been restarted successfully!"
            assert next_resp.status_code == 200
            assert next_resp.json().get("message") == "You got it"
            assert next_resp.json().get("session_status") == "complete"
            assert next_resp.json().get("remaining_attempts") == 9
        finally:
            secret_field.default_factory = original_factory
            SessionObject.model_rebuild(force=True)

    def test_restart_session_restart_active_session(self, api_client):
        username = "kacha"
        password = "asd"
        reg_resp = api_client.user_register(username, password)
        log_resp = api_client.user_login(username, password)
        ses_resp = api_client.create_session()
        assert reg_resp.status_code == 201
        assert log_resp.status_code == 200
        assert ses_resp.status_code == 201
        res_resp = api_client.http_client.post("/sessions/restart", headers={"Authorization": f"Bearer {api_client.token}"})
        assert res_resp.status_code == 409
        assert res_resp.json().get("detail") == "Session already active and running"
    
    def test_restart_session_when_session_doesnot_exit(self, api_client):
        username = "kacha"
        password = "asd"
        reg_resp = api_client.user_register(username, password)
        log_resp = api_client.user_login(username, password)
        res_resp = api_client.http_client.post("/sessions/restart", headers={"Authorization": f"Bearer {api_client.token}"})
        assert reg_resp.status_code == 201
        assert log_resp.status_code == 200
        assert res_resp.status_code == 404
        assert res_resp.json().get("detail") == "No session available for the user!"
        
    def test_restart_session_with_tampered_token(self, api_client):
        username = "kacha"
        password = "asd"
        reg_resp = api_client.user_register(username, password)
        log_resp = api_client.user_login(username, password)
        ses_resp = api_client.create_session()
        assert reg_resp.status_code == 201
        assert log_resp.status_code == 200
        assert ses_resp.status_code == 201
        api_client.token += "ding"
        res_resp = api_client.http_client.post("/sessions/restart", headers={"Authorization": f"Bearer {api_client.token}"})
        assert res_resp.status_code == 401
        assert res_resp.json().get("detail") == "Couldn't validate credentials"
