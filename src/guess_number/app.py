from fastapi import FastAPI
from guess_number.routes import cashew



bisket: FastAPI = FastAPI(title="Guess the Number")
bisket.include_router(cashew)