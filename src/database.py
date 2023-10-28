import sqlite3


class User:
    def __init__(self, name: str, bal: float, id: int = None) -> None:
        self.id = id
        self.name = name
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
        name TEXT,
        balance INTEGER
    )
            """
        )
        self.conn.commit()

    def create_user(user: User):
        pass
