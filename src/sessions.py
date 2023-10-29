from os import urandom
import base64
from models import User
from fastapi import Cookie, HTTPException
from typing import Annotated


class SessionManager:
    def __init__(self) -> None:
        self.sessions = []

    def new_session(self, user: User) -> str:
        # URL Encoded 64 random bytes - cryptographically secure :)
        token = base64.encodebytes(urandom(64)).decode()

        self.sessions.append({"user_id": user.id, "token": token})

        return token

    def find_id_from_session(self, token) -> int | None:
        for session in self.sessions:
            if session["token"] == token:
                return session["user_id"]

        return None

    def verify(self, token: Annotated[str, Cookie()]) -> int:
        user_id = self.find_id_from_session(token)

        if user_id is None:
            raise HTTPException(401, "You are not logged in")

        return user_id
