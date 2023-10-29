import sqlite3
from models import User, Stock, ApiUser


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("data.db")

    def up(self):
        cur = self.conn.cursor()
        cur.execute(
            """
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        balance REAL
    )
            """
        )
        cur.execute(
            """
    CREATE TABLE IF NOT EXISTS Stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER,
        stock_name TEXT,
        price REAL,
        amount REAL,
        timestamp INTEGER,
        FOREIGN KEY(buyer_id) REFERENCES Users(id)
    )
            """
        )
        self.conn.commit()

    def create_user(self, user: ApiUser):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO Users(username,password,balance) VALUES(?,?,?)
            """,
            (
                user.username,
                user.password,
                10_000,  # Default balance
            ),
        )
        self.conn.commit()

    def get_user_by_username(self, username: str) -> User | None:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT * FROM Users WHERE username=?
            """,
            (username,),
        )
        result = cur.fetchone()
        if result is None:
            return None
        id, username, password, balance = result

        return User(id=id, username=username, password=password, balance=balance)

    def get_user_by_id(self, id: int) -> User | None:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT * FROM Users WHERE id=?
            """,
            (id,),
        )
        result = cur.fetchone()
        if result is None:
            return None

        id, username, password, balance = result

        return User(id=id, username=username, password=password, balance=balance)

    def find_user_stocks(self, user_id: int) -> list[Stock]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, stock_name, price, amount, timestamp FROM Stocks WHERE buyer_id=?
            """,
            (user_id,),
        )
        stocks = cur.fetchall()

        user_stocks = []
        for stock in stocks:
            user_stocks.append(Stock(*stock, user_id))

        return user_stocks

    def buy_stock(self, stocks: Stock):
        total_cost = stocks.price * stocks.amount
        cur = self.conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE id=?", (stocks.buyer_id,))
        current_balance = cur.fetchone()[0]
        if current_balance < total_cost:
            raise ValueError("Insufficient funds")

        new_balance = current_balance - total_cost
        cur.execute(
            """
            UPDATE Users SET balance=? WHERE id=?
            """,
            (
                new_balance,
                stocks.buyer_id,
            ),
        )

        cur.execute(
            """
            INSERT INTO Stocks(stock_name,price,amount,timestamp,buyer_id) VALUES(?,?,?,?,?)
            """,
            (
                stocks.stock_name,
                stocks.price,
                stocks.amount,
                stocks.timestamp,
                stocks.buyer_id,
            ),
        )
        self.conn.commit()

    def sell_stock(self, stock_id: int, user_id: int):
        cur = self.conn.cursor()

        cur.execute("SELECT buyer_id FROM Users WHERE buyer_id=?", stock_id)
        buyer_id = cur.fetchone()

        if buyer_id is None:
            raise ValueError("Could not find stock by that id")

        elif buyer_id != user_id:
            print("User_id does not own that stock")

        print(user_id)
