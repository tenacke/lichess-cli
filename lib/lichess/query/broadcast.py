from __future__ import annotations

from .client import QueryClient
from lichess.base import BaseClient
from lichess.utils import Singleton


API_URL = "https://lichess.org"

class Broadcast(Singleton):
    _instance: Broadcast | None = None

    def init(self) -> None:
        self.query = QueryClient()

class BroadcastClient(BaseClient):
    _instance: BroadcastClient | None = None

    def init(self) -> None:
        self.broadcast = Broadcast()