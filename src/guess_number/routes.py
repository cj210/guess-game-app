import jwt
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from guess_number.models import GuessRequest, GameSession, UserRegister, TokenResponse
from guess_number.core import validate_guess, guess_compare

cashew: APIRouter = APIRouter()

sessions: dict[str, GameSession] = {}

users: dict[str, str] = {"kali": "abc"}

SECRET_KEY = "bisket-key-for-bisket-app"

ALGORITHM = "HS256"

@cashew.post("/register")
def user_register(user_data: UserRegister) -> dict:
    if user_data.username in users:
        raise HTTPException(401, "User already existing")
    else:
        users[user_data.username] = user_data.password

    return {
            "message": f"User {user_data.username} has been created succesfully!",
            "status": "success",
            }


@cashew.post("/login")
def user_login(user_data: UserRegister) -> dict:
    if user_data.username not in users:
        raise HTTPException(401, "Invalid Username or Password")
    if users[user_data.username] != user_data.password:
        raise HTTPException(401, "Invalid Username or Password")
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
            "sub": user_data.username,
            "exp": expire,
            }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
            "access_token": token,
            "token_type": "bearer",
            }


@cashew.post("/sessions")
def create_session() -> dict:
    session_id: str = str(uuid4())
    session: GameSession = GameSession(id=session_id)
    sessions[session_id] = session
    return {
        "session_id": session_id,
        "status": session.status,
    }

@cashew.post("/sessions/{session_id}/guesses")
def respond_to_guess(session_id: str, request: GuessRequest) -> dict:
    current_session: GameSession | None = sessions.get(session_id, None)
    if current_session:
        if current_session.status == "complete":
            raise HTTPException(409, "Not available for a completed session")
        else:
            valid_guess = validate_guess(request.guess)
            if valid_guess:
                message = guess_compare(valid_guess, current_session.secret)
                current_session.attempts -= 1
                if message == "You got it" or current_session.attempts == 0:
                    current_session.status = "complete"
                return {
                    "message": message,
                    "attempts": current_session.attempts,
                    "status": current_session.status,
                }
            else:
                raise HTTPException(422, "Unprocessible entity: Please enter number between 1 and 100")
    else:
        raise HTTPException(404, "Session doesn't exist")
        
