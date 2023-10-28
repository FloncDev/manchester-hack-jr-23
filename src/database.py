import sqlite3


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
