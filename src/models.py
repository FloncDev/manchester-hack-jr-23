from pydantic import BaseModel
from dataclasses import dataclass


class ApiUser(BaseModel):
    username: str
    password: str  # Unhashed


class ApiStock(BaseModel):
    stock_name: str
    amount: float


@dataclass
class Stock:
    stock_name: str
    price: float
    amount: float  # to support fractional shares
    timestamp: int  # UNIX timestamp (sqlite3 doesn't support datetime)
    buyer_id: int | None = None  # Foriegn key fstockor User
    id: int = None


class User(BaseModel):
    id: int
    username: str
    password: str
    balance: float
    stocks: list[Stock] = []
