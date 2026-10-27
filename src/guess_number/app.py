from fastapi import FastAPI
from guess_number.routes import palm_tree




forest: FastAPI = FastAPI(title="Guess the Number")

forest.include_router(palm_tree)
