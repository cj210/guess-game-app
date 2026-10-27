import os 
import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer




load_dotenv()

SECRET_KEY: str | None = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    raise RuntimeError("JWT key is not set")

ALGORITHM: str = "HS256"

EXPIRY_TIME: int = 15

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/login")

hasher: PasswordHash = PasswordHash.recommended()

def create_access_token(username: str) -> str:
    current_time: datetime = datetime.now(timezone.utc)
    payload: dict = {
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
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Couldn't validate credentials", headers={"WWW-Authenticate": "Bearer"})

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    payload: dict = verify_access_token(token)
    username: str | None = payload.get("sub")
    if isinstance(username, str) and username.strip():
        return username
    else:
        raise HTTPException(status_code=401, detail="Invalid / Missing subject (username)!", headers={"WWW-Authenticate": "Bearer"})
