from pydantic import BaseModel, Field
from guess_number.core import generate_secret


class UserRegister(BaseModel):

    username: str
    password: str
    
    
class ResgisterResponse(BaseModel):
    
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
    secret: int = Field(default_factory=generate_secret)
    attempts: int = 10
    status: str = "running"
    

class SessionResponse(BaseModel):
    
    detail: str
    message: str


class GuessResponse(BaseModel):
    
    detail: str
    message: str
    remaining_attempts: int
    session_status: str


class UserGuess(BaseModel):
    
    guess: str

