import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

SECRET_KEY: str | None = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    raise RuntimeError("JWT Key is not set!!")

EXPIRY_TIME: int = 15

ALGORITHM: str = "HS256"

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(username: str) -> str:
    current_time = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": current_time,
        "exp": current_time + timedelta(minutes=EXPIRY_TIME)
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def verify_access_token(token: str) -> dict:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired!", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token or credentials", headers={"WWW-Authenticate": "Bearer"})
    
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    
    payload = verify_access_token(token)

    username = payload.get("sub")

    if isinstance(username, str) and username.strip():
        return username
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid / missing subject (username)",
            headers={"WWW-Authenticate": "Bearer"}
        )