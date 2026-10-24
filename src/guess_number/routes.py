from fastapi import APIRouter, HTTPException, Depends, Form
from pwdlib import PasswordHash
from uuid import uuid4
from guess_number.models import UserRegister, RegisterResponse, UserLogin, LoginResponse, SessionResponse, GuessResponse, GuessRequest, SessionObject
from guess_number.security import create_access_token, get_current_user
from guess_number.core import guess_compare, validate_guess

cashew: APIRouter = APIRouter()

users: dict[str, str] = {}

sessions: dict[str, SessionObject] = {}

hasher: PasswordHash = PasswordHash.recommended()

@cashew.get("/me", status_code=200)
def show_profile(username: str = Depends(get_current_user)) -> dict:
    return {"username": username}

@cashew.post("/session", status_code=201, response_model=SessionResponse)
def create_session(username: str = Depends(get_current_user)) -> SessionResponse:
    if username in sessions:
        return SessionResponse(
            detail="Session exists!",
            message=f"Session already exists for User: {username}",
            session_id=sessions[username].session_id,
        )
    else:
        session_id: str = str(uuid4())
        session = SessionObject(
            session_id= session_id,
            username= username,
        )
        sessions[username] = session
        return SessionResponse(
            detail="Session created successfully!",
            message=f"Session created for User: {username}",
            session_id=session.session_id,
        )

@cashew.post("/session/{session_id}/guesses", status_code=200, response_model=GuessResponse)
def analyze_guess(session_id: str, request: GuessRequest, username: str = Depends(get_current_user)) -> GuessResponse:
    if username not in sessions:
        raise HTTPException(status_code=404, detail=f"Session doesn't exit for user {username}")
    current_session: SessionObject = sessions[username]
    if current_session.session_id != session_id:
        raise HTTPException(status_code=401, detail="Invalid User or Session")
    if current_session.status == "running":
        valid_guess: int = validate_guess(request.guess)
        if valid_guess:
            message: str = guess_compare(valid_guess, current_session.secret)
            current_session.attempts -= 1
            if message == "You got it" or current_session.attempts == 0:
                current_session.status = "complete"
            return GuessResponse(
                detail= "valid guess",
                message= message,
                attempts_remaining = current_session.attempts,
            )
        else:
            raise HTTPException(status_code=422, detail="Unprocessable input: Please enter number between 1 and 100")
    else:
        raise HTTPException(status_code=401, detail="Not available for complete sessions")

@cashew.post("/session/restart", status_code=200, response_model=SessionResponse)
def restart_session(username: str = Depends(get_current_user)):
    if username in sessions:
        current_session: SessionObject = sessions[username]
        if current_session.status == "complete":
            current_session = SessionObject(
                session_id=current_session.session_id,
                username=username
            )
            sessions[username] = current_session
            return SessionResponse(
                detail='Restart Successful!',
                message=f"Session for User: {username} has been restarted successfully!",
                session_id=current_session.session_id
            )
        else:
            raise HTTPException(status_code=409, detail="Session already active!")
    else:
        raise HTTPException(status_code=404, detail="User doesn't exist")

@cashew.post("/register", status_code=201, response_model=RegisterResponse)
def create_user(user_data: UserRegister) -> RegisterResponse:
    if user_data.username in users:
        raise HTTPException(status_code=400, detail="User already exists!")
    else:
        hashed_password: str = hasher.hash(user_data.password)
        users[user_data.username] = hashed_password
        return RegisterResponse(
            detail = "User created successfully!",
            message = f"User {user_data.username} is created!"
        )
        
        
@cashew.post("/login", status_code=200, response_model=LoginResponse) 
def user_login(username: str = Form(), password: str = Form()) -> LoginResponse:
    if username not in users:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if hasher.verify(password, users[username]):
        return LoginResponse(
            detail="User Login successfull!",
            message=f"Logged in as {username}!",
            access_token=create_access_token(username),
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
        