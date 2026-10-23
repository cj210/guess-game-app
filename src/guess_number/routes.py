from fastapi import APIRouter, HTTPException
from pwdlib import PasswordHash

from guess_number.models import UserRegister, RegisterResponse, LoginResponse
from guess_number.security import create_access_token


cashew: APIRouter = APIRouter()

hasher: PasswordHash = PasswordHash.recommended()

users: dict[str, str] = {}

@cashew.post("/register", status_code=201, response_model=RegisterResponse)
def user_register(user_data: UserRegister):
    if user_data.username in users:
        raise HTTPException(409, "Username already exists!!")
    users[user_data.username] = hasher.hash(user_data.password)
    return {
        "detail": "User creation successful",
        "message": f"User {user_data.username} created succesfully",
    }
    
@cashew.post("/login", status_code=200, response_model=LoginResponse)
def user_login(user_data: UserRegister):
    if user_data.username not in users:
        raise HTTPException(401, "Invalid Username or Password!")
    if hasher.verify(user_data.password, users[user_data.username]):
        return {
            "detail": "User login Successful!!",
            "message": f"Logged in as {user_data.username}",
            "access_token": create_access_token(user_data.username),
            "token_type": "bearer"
        }
    else:
        raise HTTPException(401, "Invalid Username or Password!")
        
    

