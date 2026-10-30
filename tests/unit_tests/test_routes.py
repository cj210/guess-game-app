import pytest
from fastapi import Response
from guess_number.routes import user_register, create_session
from guess_number.models import UserRegister, SessionObject
from guess_number.db import users, sessions
from guess_number.security import hasher


class TestUserRegister:
    
    @pytest.mark.parametrize(
        "user_name, password",
        [
            ("kacha", "asd"),
            ("12345", "&*^&)()"),
            ("$^&^%&#*&", "12345"),
        ]
    )
    def test_user_register_with_valid_input(self, user_name, password):
        user_input = UserRegister(
            username=user_name, password=password
        )
        response = user_register(user_input)

        assert users.get(user_name, password) != password
        assert hasher.verify(password, users[user_name])
        assert response.detail == "User creation successfull!"
        assert response.message == f"New user {user_name} created!"


class TestCreateSession:
    @pytest.mark.parametrize(
        "username",
        ["kacha", "12345", "Q@#$!@#"]
    )
    def test_session_creation_with_valid_data(self, username):
        response = Response(status_code=201)
        result = create_session(response, username)
        assert response.status_code == 201
        assert sessions.get(username)
        assert isinstance(sessions.get(username), SessionObject)
        assert result.detail == "Session created successfully!"
        assert result.message == f"Session created with session id: {sessions[username].session_id}"

    @pytest.mark.parametrize(
        "username",
        ["kacha", "12345", "Q@#$!@#"]
    )
    def test_session_creation_when_session_already_exists(self, username):
        response1 = Response(status_code=201)
        response2 = Response(status_code=201)
        first_attempt = create_session(response1, username)
        first_sessionid = sessions[username].session_id
        second_attempt = create_session(response2, username)
        second_sessionid = sessions[username].session_id
        assert response1.status_code == 201
        assert response2.status_code == 200
        assert first_sessionid == second_sessionid
        assert sessions.get(username) 
        assert isinstance(sessions.get(username), SessionObject)
        assert first_attempt.detail == "Session created successfully!"
        assert first_attempt.message == f"Session created with session id: {sessions[username].session_id}"
        assert second_attempt.detail == "Session already exists!"
        assert second_attempt.message == f"An active session with session id: {sessions[username].session_id} already exist"

        