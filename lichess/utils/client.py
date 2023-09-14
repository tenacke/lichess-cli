from __future__ import annotations

from .session import Session, Requestor
from .formats import JSON

API_URL = "https://lichess.org"

# Client API for lichess package

class BaseClient:
    def __init__(self, session: Session, base_url: str | None = None):
        self._r = Requestor(session, base_url or API_URL, default_fmt=JSON)


class Client(BaseClient):
    def __init__(self, token: str):
        self.session = Session(token)
        super().__init__(self.session)
