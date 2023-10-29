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
    existing_user = db.get_user_by_username(user.username)
    if existing_user:
        return {"success": False, "message": "Username already exists."}

    # Hash Password
    hashed_password = hasher.hash(user.password)

    db.create_user(ApiUser(username=user.username, password=hashed_password))

    return {"success": True}


@app.get("/me")
async def get_me(user_id: int = Depends(sessions.verify)):
    return db.get_user_by_id(user_id)


@app.post("/login")
async def login(user: ApiUser, response: Response):
    db_user = db.get_user_by_username(user.username)
    if db_user is None:
        return {"success": False, "message": "Could not find user by that name"}

    try:
        if hasher.verify(db_user.password, user.password):
            token = sessions.new_session(db_user)
            response.set_cookie(
                "token", token, max_age=60 * 60 * 24 * 7, secure=True, httponly=True
            )
            return {"success": True}
    except Exception as e:
        print(e)
        return {"success": False, "message": "Incorrect details"}


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

    return f"Purchesd {stock.amount} {stock.stock_name} stocks for {stock_price * stock.amount}"


@app.post("/sell")
async def sell_stock(id: int, user_id: int = Depends(sessions.verify)):
    try:
        db.sell_stock(id, user_id)
    except ValueError as e:
        raise HTTPException(
            401, f"That stock either does not exist or is not owned by you. {e}"
        )
    
@app.post("/sell-by-symbol")
async def sell_stock_by_symbol(stock: ApiStock, user_id: int = Depends(sessions.verify)):
    user = db.get_user_by_id(user_id)
    
    # Here, find the most recent purchase of the given stock for the user.
    # This is a simplification and might need more complex logic for a real app.
    stocks = db.find_user_stocks(user_id)
    stocks_of_symbol = [s for s in stocks if s.stock_name == stock.stock_name]
    
    if not stocks_of_symbol:
        raise HTTPException(400, f"You do not own any shares of {stock.stock_name}.")
    
    # Find the most recent purchase
    recent_stock = max(stocks_of_symbol, key=lambda x: x.timestamp)
    
    if recent_stock.amount < stock.amount:
        raise HTTPException(400, f"You do not own enough shares of {stock.stock_name} to sell.")
    
    # Use the ID of the recent stock to sell
    try:
        db.sell_stock(recent_stock.id, user_id)
        return f"Sold {stock.amount} {stock.stock_name} stocks."
    except ValueError as e:
        raise HTTPException(401, f"That stock either does not exist or is not owned by you. {e}")

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return {"success": True}

@app.get("/stock/{stock_name}")
async def get_stock(stock_name: str, _: int = Depends(sessions.verify)):
    try:
        return await stocks.get_stock_price(stock_name)
    except KeyError:
        raise HTTPException(400, "Stock could not be found")
    
@app.get("/top-stocks")
async def get_top_stocks(_: int = Depends(sessions.verify)):
    mock_stocks = [
        {"symbol": "AAPL", "price": 168.22},
        {"symbol": "MSFT", "price": 329.92},
        {"symbol": "AMZN", "price": 127.74},
        {"symbol": "TSLA", "price": 207.31},
        {"symbol": "GME", "price": 13.15},
        {"symbol": "MCD", "price": 255.8},
        {"symbol": "DIS", "price": 79.33},
        {"symbol": "NKE", "price": 97.98},
        {"symbol": "SBUX", "price": 92.02},
        {"symbol": "RBLX", "price": 30.99},
    ]
    return mock_stocks


@app.get("/news/{stock_name}")
async def get_news(stock_name: str, _: int = Depends(sessions.verify)):
    return ["Headline 1", "Headline 2"]


app.mount("/", StaticFiles(directory="src/frontend", html=True))
