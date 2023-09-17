from __future__ import annotations

from lichess import BaseClient

class Tournament(BaseClient):
    _instance: Tournament | None = None

    def init(self) -> None:
        pass