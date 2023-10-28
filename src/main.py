from fastapi import FastAPI, Response, Cookie
from fastapi.staticfiles import StaticFiles
from .database import Database
from .sessions import SessionManager
from . import stocks
from pydantic import BaseModel
from argon2 import PasswordHasher
from typing import Annotated

app = FastAPI()
hasher = PasswordHasher()
db = Database()
db.up()

sessions = SessionManager()


class CreateUser(BaseModel):
    username: str
    password: str


@app.post("/user")
async def create_user(user: CreateUser):
    # Hash Password
    hashed_password = hasher.hash(user.password)

    # TODO: Connect to DB
    return hashed_password


@app.get("/login")
async def login(user: CreateUser, response: Response):
    # TODO: Get user from database
    db_user = CreateUser(
        username="Flonc",
        password="$argon2id$v=19$m=65536,t=3,p=4$CVAW+73el4Qz+6FQQidBrw$WriVkzV/AWK2+LLK5bXNin267IRd3sAWzBiQ3fPvIjw",
    )

    if hasher.verify(db_user.password, user.password):
        response.set_cookie("token", sessions.new_session(user))
        return 200

    return 401


@app.post("/purchase")
async def purchase_stock(token: Annotated[str, Cookie()]):
    # Get user from db
    # TODO
    pass


@app.get("/test")
async def test(token: Annotated[str, Cookie()]):
    print(token)


app.mount("/", StaticFiles(directory="src/frontend", html=True))
