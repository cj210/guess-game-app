import pytest
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

from guess_number.security import create_access_token, get_current_user, verify_access_token, SECRET_KEY, ALGORITHM, EXPIRY_TIME


class TestAccessToken:
    
    @pytest.mark.parametrize(
        "dummy",
        ["duser", "12345", "_%^&*"]
    )
    def test_access_token_creation(self, dummy):

        token = create_access_token(dummy)
        assert len(token.split(".")) == 3 
        result = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = (result["exp"] - result["iat"]) / 60
        assert isinstance(result, dict)
        assert len(result.items()) == 3
        assert result["sub"] == dummy
        assert isinstance(result["iat"], int)
        assert isinstance(result["exp"], int)
        assert exp_time == EXPIRY_TIME
    
    @pytest.mark.parametrize(
        "dummy",
        ["duser", "12345", "_%^&*"]
    )
    def test_verify_access_token_valid_inputs(self, dummy):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": dummy,
            "iat": now,
            "exp": now + timedelta(minutes=EXPIRY_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        result = verify_access_token(token)
        assert result["sub"] == payload["sub"]
    
    def test_verify_access_token_couldnot_validate_credentials(self):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": "dummy",
            "iat": now,
            "exp": now + timedelta(minutes=EXPIRY_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            verify_access_token(token+"ding")
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Couldn't validate credentials"
        assert exc_info.value.headers is not None
        assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"
    
    def test_verify_access_token_invalid_token(self):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": "dummy",
            "iat": now,
            "exp": now, 
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            verify_access_token(token)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid or expired token"
        assert exc_info.value.headers is not None
        assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"
            
    @pytest.mark.parametrize(
        "dummy",
        ["duser", "12345", "_%^&*"]
    )
    def test_get_current_user_with_valid_inputs(self, dummy):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": dummy,
            "iat": now,
            "exp": now + timedelta(minutes=EXPIRY_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        result = get_current_user(token)
        assert result == dummy
    
    def test_get_current_user_with_empty_sub(self):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": "",
            "iat": now,
            "exp": now + timedelta(minutes=EXPIRY_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid / Missing subject (username)!"
        assert exc_info.value.headers is not None
        assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"
        
    def test_get_current_user_with_no_sub_claim(self):
        now = datetime.now(timezone.utc)
        payload = {
            "iat": now,
            "exp": now + timedelta(minutes=EXPIRY_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid / Missing subject (username)!"
        assert exc_info.value.headers is not None
        assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"

        
    def test_get_current_user_with_blank_sub_clain(self):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": "              ",
            "iat": now,
            "exp": now + timedelta(minutes=EXPIRY_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid / Missing subject (username)!"
        assert exc_info.value.headers is not None
        assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"


        
        
