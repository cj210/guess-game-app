from pydantic import BaseModel


class UserRegister(BaseModel):

    username: str
    password: str
    
    
class UserLogin(BaseModel):

    username: str
    password: str


class RegisterResponse(BaseModel):

    detail: str
    message: str


class LoginResponse(BaseModel):
    detail: str
    message: str
    access_token: str
    token_type: str = "bearer"



