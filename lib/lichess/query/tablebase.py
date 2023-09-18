from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Tablebase(Singleton):
    _instance: Tablebase | None = None

    def init(self) -> None:
        pass

class TablebaseClient(BaseClient):
    _instance: TablebaseClient | None = None

    def init(self) -> None:
        self.broadcast = Tablebase()