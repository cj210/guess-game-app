from pydantic import BaseModel, Field
from guess_number.core import generate_secret


class UserRegister(BaseModel):
    
    username: str
    password: str


class RegisterResponse(BaseModel):
    
    detail: str
    message: str


class UserLogin(BaseModel):
    
    username: str
    password: str

    
class LoginResponse(BaseModel):
    
    detail: str
    message: str
    access_token: str
    token_type: str = "bearer"


class SessionObject(BaseModel):
    
    session_id: str
    username: str
    secret: int = Field(default_factory=generate_secret)
    attempts: int = 10
    status: str = "running"


class SessionResponse(BaseModel):
    
    detail: str
    message: str
    session_id: str

class GuessRequest(BaseModel):
    
    guess: str


class GuessResponse(BaseModel):
    
    detail: str
    message: str
    attempts_remaining: int
    