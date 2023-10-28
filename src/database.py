import sqlite3


class User:
    def __init__(self, username: str, password: str, bal: float, id: int = None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.bal = bal


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
        bal INTEGER
    )
            """
        )
        self.conn.commit()

    def create_user(self, user: User):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO Users(username,bal)
            VALUES(?,?)
            """,
            user.username,
            user.password,
            user.bal
        )
        self.conn.commit()