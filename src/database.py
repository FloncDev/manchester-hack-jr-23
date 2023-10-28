import sqlite3

class User:
    def __init__(self, username: str, password: str, bal: float, id: int = None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.bal = bal

class Stocks:
    def __init__(self, stock_name: str, price: float, amount: float, timestamp: int, buyer_id: id = None) -> None:
        self.stock_name = stock_name
        self.price = price
        self.amount = amount
        self.timestamp = timestamp
        self.buyer_id = buyer_id

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
        bal REAL
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

    def create_user(self, user: User):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO Users(username,password,bal) VALUES(?,?,?)
            """,
            (user.username,
            user.password,
            user.bal,)
        )
        self.conn.commit()
    
    def get_user_by_username(self, user: User):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT * FROM Users WHERE username=?
            """,
            (user.username,)
        )
        result = cur.fetchone()
        return User(
            result[1],
            result[2],
            result[3],
            result[0]
        )

    def get_user_by_id(self, user: User):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT * FROM Users WHERE id=?
            """,
            (user.id,)
        )
        result = cur.fetchone()
        return User(
            result[1],
            result[2],
            result[3],
            result[0]
        )
    
    def find_user_stocks(self, user: User):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT stock_name, amount, timestamp FROM Stocks WHERE buyer_id=?
            """,
            (user.id,)
        )
        stocks = cur.fetchall()
        return stocks
    
    def buy_stock(self, stocks: Stocks):
        total_cost = stocks.price * stocks.amount
        cur = self.conn.cursor()
        cur.execute("SELECT bal FROM Users WHERE id=?", (stocks.buyer_id,))
        current_balance = cur.fetchone()[0]
        if current_balance < total_cost:
            raise ValueError("Insufficient funds")

        new_balance = current_balance - total_cost
        cur.execute(
            """
            UPDATE Users SET bal=? WHERE id=?
            """,
            (new_balance, stocks.buyer_id))

        cur.execute(
            """
            INSERT INTO Stocks(stock_name,amount,timestamp,buyer_id) VALUES(?,?,?,?)
            """,
            (stocks.stock_name,
             stocks.amount,
             stocks.timestamp,
             stocks.buyer_id,)
        )
        self.conn.commit()