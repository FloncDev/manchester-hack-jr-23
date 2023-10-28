from uuid import uuid4, UUID


class SessionManager:
    def __init__(self) -> None:
        self.sessions = []

    def new_session(self, user) -> UUID:
        token = uuid4()

        self.sessions.append({"user_id": user.username, "token": token})

        return token

    def find_id_from_session(self, token) -> int:
        for session in self.sessions:
            if session["token"] == token:
                return session["user_id"]

        return None
