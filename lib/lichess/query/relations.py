from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Relations(Singleton):
    _instance: Relations | None = None

    def init(self) -> None:
        pass

class RelationsClient(BaseClient):
    _instance: RelationsClient | None = None

    def init(self) -> None:
        self.broadcast = Relations()