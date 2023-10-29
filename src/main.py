from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from .database import Database
from .sessions import SessionManager
from . import stocks
from .models import ApiStock, ApiUser, Stock
from argon2 import PasswordHasher
import time

app = FastAPI()
hasher = PasswordHasher()
db = Database()
db.up()

sessions = SessionManager()


@app.post("/user")
async def create_user(user: ApiUser):
    # Hash Password
    hashed_password = hasher.hash(user.password)

    db.create_user(ApiUser(username=user.username, password=hashed_password))

    return hashed_password


@app.get("/me")
async def get_me(user_id: int = Depends(sessions.verify)):
    return db.get_user_by_id(user_id)


@app.post("/login")
async def login(user: ApiUser, response: Response):
    db_user = db.get_user_by_username(user.username)
    if db_user is None:
        raise HTTPException(401, "Could not find user by that name")

    try:
        if hasher.verify(db_user.password, user.password):
            token = sessions.new_session(db_user)
            response.set_cookie(
                "token", token, max_age=60 * 60 * 24 * 7, secure=True, httponly=True
            )
            return token

    except Exception as e:
        print(e)
        raise HTTPException(401, "Incorrect details")


@app.post("/purchase")
async def purchase_stock(stock: ApiStock, user_id: int = Depends(sessions.verify)):
    user = db.get_user_by_id(user_id)

    stock_price = await stocks.get_stock_price(stock.stock_name)
    purchase_order = Stock(
        stock.stock_name, stock_price, stock.amount, int(time.time()), user.id
    )

    try:
        db.buy_stock(purchase_order)
    except ValueError:
        raise HTTPException(400, f"You do not have enough money required.")

    return f"Purchesd {stock.amount} {stock.stock_name} stocks for {stock_price}"


@app.get("/stocks")
async def get_stocks(user_id: int = Depends(sessions.verify)):
    return db.find_user_stocks(user_id)


@app.post("/sell")
async def sell_stock(id: int):
    pass


@app.get("/test")
async def test(user_id: int = Depends(sessions.verify)):
    print(user_id)


app.mount("/", StaticFiles(directory="src/frontend", html=True))
