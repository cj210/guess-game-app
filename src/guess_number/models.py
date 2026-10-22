from dataclasses import dataclass, field
from pydantic import BaseModel
from guess_number.core import generate_secret


@dataclass
class GameSession:
    
    id: str
    player: str
    secret: int = field(default_factory=generate_secret)
    attempts: int = 5
    status: str = "running"


class GuessRequest(BaseModel):
    
    guess: str


class UserRegister(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
