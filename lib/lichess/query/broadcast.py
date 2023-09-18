from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Broadcast(Singleton):
    _instance: Broadcast | None = None

    def init(self) -> None:
        pass

class BroadcastClient(BaseClient):
    _instance: BroadcastClient | None = None

    def init(self) -> None:
        self.broadcast = Broadcast()