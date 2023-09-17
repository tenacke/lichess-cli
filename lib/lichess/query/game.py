from __future__ import annotations

from lichess import BaseClient

class Game(BaseClient):
    _instance: Game | None = None

    def init(self) -> None:
        pass