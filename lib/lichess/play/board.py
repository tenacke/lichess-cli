from __future__ import annotations

from lichess import BaseClient

class Board(BaseClient):
    _instance: Board | None = None

    def init(self) -> None:
        pass