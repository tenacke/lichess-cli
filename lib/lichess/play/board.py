from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Board(Singleton):
    _instance: Board | None = None

    def init(self) -> None:
        pass

class BoardClient(BaseClient):
    _instance: BoardClient | None = None

    def init(self) -> None:
        self.broadcast = Board()