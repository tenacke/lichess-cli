from __future__ import annotations

from lichess import BaseClient

class Puzzle(BaseClient):
    _instance: Puzzle | None = None

    def init(self) -> None:
        pass