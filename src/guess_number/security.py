import os 
import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta


load_dotenv()

SECRET_KEY: str = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    raise RuntimeError("JWT key is not set !!")

ALGORITHM: str = "HS256"

EXPIRY_TIME: int = 15

def create_access_token(username: str) -> str:
    current_time = datetime.now(timezone.utc)

    payload = {
            "sub": username,
            "iat": current_time,
            "exp": current_time + timedelta(minutes=EXPIRY_TIME),
            }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )







