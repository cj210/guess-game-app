import os 
import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv



load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    raise RuntimeError("JWT key is not set!!")

ALGORITHM = "HS256"

EXPIRY_MINUTES = 15

def create_access_token(username: str) -> str:
    
    now = datetime.now(timezone.utc)

    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(minutes=EXPIRY_MINUTES)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



