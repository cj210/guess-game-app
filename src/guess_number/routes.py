from fastapi import APIRouter, HTTPException, Depends, Form, Response
from uuid import uuid4
from guess_number.models import (
    UserRegister, ResgisterResponse, UserLogin, LoginResponse, SessionObject, SessionResponse, GuessResponse, UserGuess
)
from guess_number.db import users, sessions
from guess_number.core import validate_guess, guess_compare
from guess_number.security import create_access_token, get_current_user, hasher


palm_tree: APIRouter = APIRouter()


            
@palm_tree.post("/register", status_code=201, response_model=ResgisterResponse)
def user_register(user_data: UserRegister) -> ResgisterResponse:

    if user_data.username in users:
        raise HTTPException(status_code=409, detail="User already exist!")
    else:
        hashed_password: str = hasher.hash(user_data.password)
        users[user_data.username] = hashed_password
        return ResgisterResponse(
            detail="User creation successfull!",
            message=f"New user {user_data.username} created!"
        )

@palm_tree.post("/login", status_code=200, response_model=LoginResponse)
def user_login(username: str = Form(), password: str = Form()) -> LoginResponse:
    if username in users:
        if hasher.verify(password, users[username]):
            return LoginResponse(
                detail="User Login successfull!", 
                message=f"Logged in as {username}!",
                access_token=create_access_token(username)
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password!")
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password!")
    
@palm_tree.post("/sessions", status_code=201, response_model=SessionResponse)
def create_session(response: Response, username: str = Depends(get_current_user)) -> SessionResponse:
    
    if username in sessions:
        response.status_code=200
        session: SessionObject = sessions[username]
        return SessionResponse(
            detail="Session already exists!",
            message=f"An active session with session id: {session.session_id} already exist"
        )
    else:
        session: SessionObject = SessionObject(
            session_id= str(uuid4()),
        )
        sessions[username] = session
        return SessionResponse(
            detail="Session created successfully!",
            message=f"Session created with session id: {session.session_id}"
        )
    
@palm_tree.post("/sessions/{session_id}/guesses", status_code=200, response_model=GuessResponse)
def respond_to_guess(session_id: str, user_data: UserGuess, username: str = Depends(get_current_user)) -> GuessResponse:
    if username in users:
        if username in sessions:
            if sessions[username].session_id == session_id:
                current_session: SessionObject = sessions[username]
                if current_session.status == "running":
                    guess: str = user_data.guess
                    valid_guess: int = validate_guess(guess)
                    if valid_guess:
                        message: str = guess_compare(valid_guess, current_session.secret)
                        current_session.attempts -= 1
                        if current_session.attempts == 0 or message == "You got it":
                            current_session.status = "complete"
                        return GuessResponse(
                            detail= "Its a valid guess",
                            message= message,
                            remaining_attempts = current_session.attempts,
                            session_status= current_session.status
                        )
                    else:
                        raise HTTPException(status_code=422, detail="Unprocessable data. Please enter number between 1 and 100!")
                else:
                    raise HTTPException(status_code=409, detail="No active session running for current user. Please restart game")
            else:
                raise HTTPException(status_code=404, detail="Invalid session ID")
        else:
            raise HTTPException(status_code=404, detail="No session available for current user")
    else:
        raise HTTPException(status_code=401, detail="Invalid user!")

@palm_tree.post("/sessions/restart", status_code=200, response_model=SessionResponse)
def restart_session(username: str = Depends(get_current_user)) -> SessionResponse:
    if username in users:
        if username in sessions:
            current_session: SessionObject = sessions[username]
            if current_session.status == "complete":
                session: SessionObject = SessionObject(
                    session_id=current_session.session_id
                )
                sessions[username] = session
                return SessionResponse(
                    detail= "Session restarted successfully!",
                    message=f"Session: {session.session_id} has been restarted successfully!"
                )
            else:
                raise HTTPException(status_code=409, detail=f"Session already active and {current_session.status}")
        else:
            raise HTTPException(status_code=404, detail="No session available for the user!")
    else:
        raise HTTPException(status_code=401, detail="Invalid user!")