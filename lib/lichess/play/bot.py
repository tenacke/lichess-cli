from __future__ import annotations

from lichess import BaseClient

class Bot(BaseClient):
    _instance: Bot | None = None

    def init(self) -> None:
        pass