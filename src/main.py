from fastapi import FastAPI
from .database import Database, User

app = FastAPI()
db = Database()
db.up()
db.create_user(User("PierogiMuncher", "abc123", 10000))

@app.get("/")
async def read_root():
    return "Hello, World"
