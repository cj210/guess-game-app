from guess_number.models import SessionObject, LoginResponse


class TestModels:
    
    def test_verify_session_object_defaults(self):
        session = SessionObject(session_id="fake_id")
        assert session.secret > 0 and session.secret < 101
        assert session.status == "running"
        assert session.attempts == 10
    
    def test_login_response_default_value(self):
        response = LoginResponse(
            detail="fake_detail",
            message="fake_message",
            access_token="fake_access_token"
        )
        assert response.token_type == "bearer"
    