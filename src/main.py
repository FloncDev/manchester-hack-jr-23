from fastapi import FastAPI
from .database import Database

app = FastAPI()
db = Database()
db.up()


@app.get("/")
async def read_root():
    return "Hello, World"
