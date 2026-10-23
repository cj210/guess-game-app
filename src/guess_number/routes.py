from fastapi import APIRouter, HTTPException
from pwdlib import PasswordHash


from guess_number.models import UserRegister, RegisterResponse, UserLogin, LoginResponse
from guess_number.security import create_access_token 



cashew: APIRouter = APIRouter()

users: dict[str, str] = {}

hasher: PasswordHash = PasswordHash.recommended()

@cashew.post("/register", status_code=201, response_model=RegisterResponse)
def user_register(user_data: UserRegister) -> RegisterResponse:
    if user_data.username in users:
        raise HTTPException(409, "User already exists!!")
    else:
        hashed_password = hasher.hash(user_data.password)
        users[user_data.username] = hashed_password

        return RegisterResponse(
                detail = "User creation successful!",
                message = f"User {user_data.username} created!",
                )

@cashew.post("/login", status_code=200, response_model=LoginResponse)
def user_login(user_data: UserLogin) -> LoginResponse:
    if user_data.username not in users:
        raise HTTPException(401, "Invalid Username or Password")
    if hasher.verify(user_data.password, users[user_data.username]):
        return LoginResponse(
                detail = "Login successful!",
                message = f"Logged in as {user_data.username}",
                access_token = create_access_token(user_data.username),
                )
    else:
        raise HTTPException(401, "Invalid Username or Password")
        




